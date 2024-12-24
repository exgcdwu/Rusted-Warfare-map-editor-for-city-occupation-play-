import numpy as np
import zlib
import gzip
import base64

def ndarray_from_text_packed(text:str, encoding:str, compression:str)->np.ndarray:
    if encoding == "base64":
        nmatrix = base64.b64decode(text)
    else:
        raise NotImplementedError(f": encoding type {encoding} not supported")
    if compression == "zlib":
        nmatrix = zlib.decompress(nmatrix)
    elif compression == "gzip":
        nmatrix = gzip.decompress(nmatrix)
    elif compression == None:
        pass
    else:
        raise NotImplementedError(f": Compression type {compression} not supported")
    nmatrix = np.frombuffer(nmatrix, dtype=np.uint32)
    nmatrix = np.copy(nmatrix)
    return nmatrix

def text_packed_from_ndarray(ndarray_now:np.ndarray, encoding:str, compression:str):
    text_packed = ndarray_now.flatten().tobytes()
    if compression == "zlib":
        text_packed = zlib.compress(text_packed)
    elif compression == "gzip":
        text_packed = gzip.compress(text_packed)
    elif compression == None:
        pass
    else:
        raise NotImplementedError(f": Compression type {compression} not supported")
    if encoding == "base64":
        text_packed = base64.b64encode(text_packed).decode(encoding="utf-8")
    else:
        raise NotImplementedError(f": encoding type {encoding} not supported")
    return text_packed

def indentstr_Tab(str_now:str)->str:
    str_list = str_now.split("\n")
    for i in range(0, len(str_list)):
        str_list[i] = "\t" + str_list[i]
    str_list[0] = str_list[0][1:]
    str_ans = "\n".join(str_list)
    return str_ans

def str_slash_to_dot(str_now:str)->str:
    str_list = str_now.split("/")
    str_now = str_list[-1]
    str_list = str_now.split(".")
    str_now = str_list[0]
    return str_now

def map_characters(input_str, char_map):
    return ''.join([char_map.get(char, char) for char in input_str])

def blanktoNone(input_str):
    return input_str if input_str != '' else None