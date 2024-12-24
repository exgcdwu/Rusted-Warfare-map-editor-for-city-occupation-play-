#ifndef UTILITY_HPP

#define UTILITY_HPP

#include <memory>

#define pi(x); std::cout << x << ' ';
#define etr(); std::cout << std::endl;
#define petr(x); std::cout << x << std::endl;
#define pch(d,c,x); if(d){std::cout << c << ':' << x << std::endl;}

const uint32_t RGB_mul = 256 * 256 * 256;

std::unique_ptr<size_t[]> new_index_jump_shape(size_t , std::unique_ptr<size_t[]>& );
std::unique_ptr<size_t[]> new_index_jump_shape_vector(size_t , std::vector<size_t>& );

void throw_index(size_t , size_t , int );

inline void check_leak(size_t index_now, size_t index_max){
#ifdef DEBUG
    if (index_now >= index_max){
        throw std::runtime_error("check_leak");
    }
#endif
}

template<class T1, class T2>
void runtime_error_s(std::string s_name, size_t dim, size_t dim_now, T1* thing, T2* n_shape){
    if (dim != dim_now){
        throw std::runtime_error(s_name + " : dim error(T:" + std::to_string(dim) + ",F:" + std::to_string(dim_now) + ')');
    }
    for (size_t i = 0 ; i < dim ; ++i){
        if (thing[i] != n_shape[i]){
            throw std::runtime_error(s_name + " : shape(" + std::to_string(i) + ") error, (T:" + std::to_string(n_shape[i]) + ",F:" + std::to_string(thing[i]) + ')');
        }
    }
}

uint32_t sRGB_square2(uint8_t* , uint8_t* );
double sRGB_square2(double*, double*);
double sRGB_square2(double* , uint8_t* );
uint32_t sRGB_sub_abs(uint8_t* , uint8_t* );

#endif // UTILITY_HPP