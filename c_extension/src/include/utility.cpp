#include <cmath>
#include <algorithm>
#include <array>
#include <vector>
#include <cstdint>
#include <string>
#include <cstring>
#include <memory>
#include <cfloat>
#include <iostream>
#include "utility.hpp"

std::unique_ptr<size_t[]> new_index_jump_shape(size_t dim, std::unique_ptr<size_t[]>& shape){
    std::unique_ptr<size_t[]> index_jump_shape = std::make_unique<size_t[]>(dim);
    size_t mul_now = 1;
    for (size_t i = dim - 1 ; i < dim; --i){
        index_jump_shape[i] = mul_now;
        mul_now *= shape[i];
    }
    return index_jump_shape;
}

std::vector<size_t> new_index_jump_shape_vector(std::vector<size_t>& shape){
    std::vector<size_t> index_jump_shape(shape.size());
    size_t mul_now = 1;
    for (size_t i = shape.size() - 1 ; i < shape.size(); --i){
        index_jump_shape[i] = mul_now;
        mul_now *= shape[i];
    }
    return index_jump_shape;
}

void throw_index(size_t index, size_t sum, int code){
    if (index >= sum){
        std::cout << "throw code:" << code << "(" << index << ":T," << sum << ":F)" << std::endl;
        throw std::runtime_error("");
    }
}

uint32_t sRGB_square2(uint8_t* rgb1, uint8_t* rgb2) {
    int32_t rs = static_cast<int32_t>(rgb1[0]) - rgb2[0], gs = static_cast<int32_t>(rgb1[1]) - rgb2[1], bs = static_cast<int32_t>(rgb1[2]) - rgb2[2];
    return static_cast<uint32_t>(rs * rs + gs * gs + bs * bs);
}

double sRGB_square2(double* rgb1, double* rgb2) {
    double rs = rgb1[0] - rgb2[0], gs = rgb1[1] - rgb2[1], bs = rgb1[2] - rgb2[2];
    return rs * rs + gs * gs + bs * bs;
}

double sRGB_square2(double* rgb1, uint8_t* rgb2) {
    double rs = rgb1[0] - rgb2[0], gs = rgb1[1] - rgb2[1], bs = rgb1[2] - rgb2[2];
    return rs * rs + gs * gs + bs * bs;
}

uint32_t sRGB_sub_abs(uint8_t* rgb1, uint8_t* rgb2) {
    int32_t rs = static_cast<int32_t>(rgb1[0]) - rgb2[0], gs = static_cast<int32_t>(rgb1[1]) - rgb2[1], bs = static_cast<int32_t>(rgb1[2]) - rgb2[2];
    return static_cast<uint32_t>(std::abs(rs) + std::abs(gs) + std::abs(bs));
}

