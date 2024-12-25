cmake_minimum_required(VERSION 3.4)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

set(C_EXTENSION_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/include")
set(C_EXTENSION_SRC_DIR "${CMAKE_SOURCE_DIR}/src")
set(C_EXTENSION_SRC_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/src/include")

add_definitions(-DDEBUG)

include_directories(${C_EXTENSION_INCLUDE_DIR})
include_directories(${C_EXTENSION_SRC_INCLUDE_DIR})

add_library(CIE2000 STATIC "${C_EXTENSION_SRC_INCLUDE_DIR}/CIE2000.cpp")
add_library(utility STATIC "${C_EXTENSION_SRC_INCLUDE_DIR}/utility.cpp")

find_package(pybind11 CONFIG REQUIRED)
include_directories(${pybind11_INCLUDE_DIRS})

project(c_extension)

set(RWMAPAUTOC_SRC_LAYER "${C_EXTENSION_SRC_DIR}/rwmapautoc/layerauto.cpp")
set(RWMAPAUTOC_SRC_TILESET "${C_EXTENSION_SRC_DIR}/rwmapautoc/tilesetauto.cpp")
set(RWMAPAUTOC_SRC_LIST "${RWMAPAUTOC_SRC_LAYER}" "${RWMAPAUTOC_SRC_TILESET}")

add_library(rwmapautoc_func STATIC "${RWMAPAUTOC_SRC_LIST}")
target_link_libraries(rwmapautoc_func PRIVATE CIE2000)
target_link_libraries(rwmapautoc_func PRIVATE utility)
target_link_libraries(rwmapautoc_func PRIVATE pybind11::module)

set(RWMAPAUTOC_SRC_CORE "${C_EXTENSION_SRC_DIR}/rwmapautoc/core.cpp")
pybind11_add_module(rwmapautoc "${RWMAPAUTOC_SRC_CORE}")

target_link_libraries(rwmapautoc PRIVATE rwmapautoc_func)
target_link_libraries(rwmapautoc PRIVATE CIE2000)
target_link_libraries(rwmapautoc PRIVATE utility)
target_link_libraries(rwmapautoc PRIVATE pybind11::module)







