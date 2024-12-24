#include <pybind11/pybind11.h>

#include "rwmapautoc_core.hpp"

namespace py = pybind11;

PYBIND11_MODULE(rwmapautoc, m) {
    bind_module_layerauto(m);
    bind_module_tilesetauto(m);
}