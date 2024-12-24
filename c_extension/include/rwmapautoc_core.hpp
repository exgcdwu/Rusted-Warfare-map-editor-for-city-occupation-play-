#ifndef RWMAPAUTOC_CORE_HPP
#define RWMAPAUTOC_CORE_HPP

#include <pybind11/pybind11.h>

void bind_module_layerauto(pybind11::module_&);
void bind_module_tilesetauto(pybind11::module_&);

#endif // RWMAPAUTOC_CORE_HPP