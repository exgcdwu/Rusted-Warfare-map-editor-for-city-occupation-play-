"""
asteval 状态管理工具
用于安全执行 aeval 表达式，并在执行后自动恢复状态
"""

from contextlib import contextmanager
from copy import deepcopy, copy
import pickle


@contextmanager
def safe_aeval_context(aeval):
    """
    安全的 aeval 上下文管理器
    执行完毕后自动恢复 symtable 状态
    
    用法:
        with safe_aeval_context(aeval):
            result = aeval('[ti for ti in range(13)]')
        # 退出后，aeval.symtable 自动恢复到执行前的状态
    """
    # 保存当前状态（浅拷贝）
    saved_state = aeval.symtable.copy()
    
    try:
        yield aeval
    finally:
        # 恢复状态
        aeval.symtable.clear()
        aeval.symtable.update(saved_state)


@contextmanager
def safe_aeval_context_deep(aeval):
    """
    安全的 aeval 上下文管理器（深拷贝版本）
    当 symtable 中的值本身会被修改时（如列表元素变化）使用
    
    用法:
        with safe_aeval_context_deep(aeval):
            result = aeval('some_list.append(1)')
        # 退出后，aeval.symtable 完全恢复到执行前的状态
    """
    # 保存当前状态（深拷贝，跳过无法序列化的对象）
    saved_state = _safe_deepcopy_dict(aeval.symtable)
    
    try:
        yield aeval
    finally:
        # 恢复状态
        aeval.symtable.clear()
        aeval.symtable.update(saved_state)


def _safe_deepcopy_dict(d):
    """
    安全地深拷贝字典，跳过无法 pickle 的对象
    """
    result = {}
    for key, value in d.items():
        try:
            # 测试是否可 pickle
            pickle.dumps(value)
            result[key] = deepcopy(value)
        except (TypeError, pickle.PicklingError):
            # 无法复制的对象，保留引用（添加警告）
            print(f"Warning: Cannot deepcopy '{key}', using reference")
            result[key] = value
    return result


def execute_and_clean_comprehension(aeval, expr):
    """
    执行表达式，并自动清理列表推导式可能泄漏的循环变量
    
    用法:
        result = execute_and_clean_comprehension(aeval, '[ti for ti in range(13)]')
        # 'ti' 会被自动清理
    """
    # 记录执行前的键
    before_keys = set(aeval.symtable.keys())
    
    # 执行表达式
    result = aeval(expr)
    
    # 找出新增的键
    after_keys = set(aeval.symtable.keys())
    new_keys = after_keys - before_keys
    
    # 清理可能是列表推导式泄漏的循环变量（单字母小写变量）
    for key in list(new_keys):
        if len(key) == 1 and key.islower():
            del aeval.symtable[key]
    
    return result


class AevalGuard:
    """
    aeval 状态守护类
    提供更精细的控制
    
    用法:
        guard = AevalGuard(aeval)
        guard.save()
        result = guard.execute('[ti for ti in range(13)]')
        guard.restore()  # 手动恢复
        # 或者使用 with 语句
        with guard:
            result = guard.execute('[ti for ti in range(13)]')
    """
    
    def __init__(self, aeval):
        self.aeval = aeval
        self._saved_state = None
        self._saved_version = 0
        self._version = 0
        
        # 包装 symtable 的修改方法
        self._wrap_symtable()
    
    def _wrap_symtable(self):
        """轻量级包装，只监控变化，不代理所有操作"""
        original_setitem = self.aeval.symtable.__setitem__
        original_delitem = self.aeval.symtable.__delitem__
        original_clear = self.aeval.symtable.clear
        original_update = self.aeval.symtable.update
        original_pop = self.aeval.symtable.pop
        original_popitem = self.aeval.symtable.popitem
        
        def _increment():
            self._version += 1
        
        def _wrapped_setitem(key, value):
            _increment()
            return original_setitem(key, value)
        
        def _wrapped_delitem(key):
            _increment()
            return original_delitem(key)
        
        def _wrapped_clear():
            _increment()
            return original_clear()
        
        def _wrapped_update(*args, **kwargs):
            _increment()
            return original_update(*args, **kwargs)
        
        def _wrapped_pop(key, default=None):
            _increment()
            return original_pop(key, default)
        
        def _wrapped_popitem():
            _increment()
            return original_popitem()
        
        # 用闭包替换方法
        self.aeval.symtable.__setitem__ = _wrapped_setitem
        self.aeval.symtable.__delitem__ = _wrapped_delitem
        self.aeval.symtable.clear = _wrapped_clear
        self.aeval.symtable.update = _wrapped_update
        self.aeval.symtable.pop = _wrapped_pop
        self.aeval.symtable.popitem = _wrapped_popitem
    
    def save(self):
        """保存当前状态"""
        # 使用深拷贝，跳过无法复制的对象
        self._saved_state = _safe_deepcopy_dict(self.aeval.symtable)
        self._saved_version = self._version
        return self
    
    def has_changed(self):
        """检查是否发生了变化"""
        return self._version != self._saved_version
    
    def restore(self):
        """恢复到保存的状态"""
        if self._saved_state is not None:
            self.aeval.symtable.clear()
            self.aeval.symtable.update(self._saved_state)
            self._version = self._saved_version
        return self
    
    def execute(self, expr):
        """执行表达式"""
        return self.aeval(expr)
    
    def __enter__(self):
        self.save()
        return self
    
    def __exit__(self, *args):
        if self.has_changed():
            self.restore()


# 便捷函数
def safe_eval(aeval, expr, deep=False):
    """
    安全执行 aeval 表达式，自动恢复状态
    
    用法:
        result = safe_eval(aeval, '[ti for ti in range(13)]')
        # aeval 状态自动恢复
    """
    if deep:
        with safe_aeval_context_deep(aeval):
            return aeval(expr)
    else:
        with safe_aeval_context(aeval):
            return aeval(expr)


def clean_eval(aeval, expr):
    """
    执行表达式并自动清理列表推导式泄漏的变量
    
    用法:
        result = clean_eval(aeval, '[ti for ti in range(13)]')
        # 'ti' 被自动清理
    """
    return execute_and_clean_comprehension(aeval, expr)