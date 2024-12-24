#include <vector>
#include <cstdint>
#include <cstdlib>
#include <memory>
#include <cfloat>
#include <string>
#include <cstring>
#include <iostream>
#include <algorithm>
#include <unordered_set>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
namespace py = pybind11;

#include "CIE2000.hpp"
#include "utility.hpp"
#include "rwmapautoc_core.hpp"

struct RGB {
    uint8_t r, g, b;
};

struct HSV {
    double h, s, v;
    size_t oi;
};

HSV RGBtoHSV(const RGB& rgb) {
    double r = rgb.r / 255.0;
    double g = rgb.g / 255.0;
    double b = rgb.b / 255.0;

    double max_val = std::max({r, g, b});
    double min_val = std::min({r, g, b});
    double delta = max_val - min_val;

    HSV hsv;
    hsv.v = max_val;

    if (max_val == 0) {
        hsv.h = 0;
        hsv.s = 0;
    } else {
        hsv.s = delta / max_val;

        if (r == max_val) {
            hsv.h = 60 * ((g - b) / delta);
        } else if (g == max_val) {
            hsv.h = 60 * ((b - r) / delta + 2);
        } else {
            hsv.h = 60 * ((r - g) / delta + 4);
        }

        if (hsv.h < 0) {
            hsv.h += 360;
        }
    }

    return hsv;
}

bool HSV_compare_H(HSV& a, HSV& b){
    return a.h < b.h;
} 

bool HSV_compare_S_b(HSV& a, HSV& b){
    return a.s > b.s;
} 

bool HSV_compare_S(HSV& a, HSV& b){
    return a.s < b.s;
}

bool HSV_compare_V_b(HSV& a, HSV& b){
    return a.v > b.v;
} 

const double S_power = 1, V_power = 1;

const double threshold_S = 0.15;
const double threshold_V = 0.15;

bool HSV_compare_SV(HSV& a, HSV& b){
    return a.s * S_power + a.v * V_power < b.s * S_power + b.v * V_power;
} 

char int4_hex(uint8_t i4){
    if (i4 >= 10){
        return 'a' + (i4 - 10);
    }
    else{
        return '0' + i4;
    }
}

std::string int8_hex(uint8_t i8){
    std::string hex = std::string({int4_hex(i8 / 16), int4_hex(i8 % 16)});
    return hex;
}

void print_rgb(uint8_t *ptr){
    std::cout << '#' << int8_hex(*ptr) << int8_hex(*(ptr + 1)) << int8_hex(*(ptr + 2));
}

void tilesetauto_average(uint8_t* image, uint8_t* result, const size_t n, const size_t ny, const size_t ix, const size_t iy, const size_t tx, const size_t ty, const int stopnum, const std::time_t rand_seed, const size_t limit_cycle, const int mode_code, bool isverbose = false, bool isdebug = false){
    if (isverbose){
        std::cout << "tilesetauto average mode: process..." << std::endl;
        std::cout << "    image:(" << ix << "," << iy << "," << 3 << ")" << std::endl;
        std::cout << "    tileset_size:(" << n << "," << tx << "," << ty << "," << 3 << ")" << std::endl;
        std::cout << "    column:" << ny << ",stopnum:" << stopnum << ",mode_code:" << mode_code << ",limit_cycle:" << limit_cycle << ",rand_seed:" << rand_seed << ",ix:" << ix << ",iy:" << iy << ",tx:" << tx << ",ty:" << ty << ",n:" << n << std::endl;
    }

    if (isverbose){
        std::cout << "tilesetauto average: initialization..." << std::endl;
    }

    std::unique_ptr<size_t[]> image_num = std::make_unique<size_t[]>(3);
    image_num[0] = ix;
    image_num[1] = iy;
    image_num[2] = 3;
    auto image_jump = new_index_jump_shape(3, image_num);
    size_t image_sum = image_jump[0] * image_num[0];

    std::unique_ptr<size_t[]> result_num = std::make_unique<size_t[]>(4);
    result_num[0] = n;
    result_num[1] = tx;
    result_num[2] = ty;
    result_num[3] = 3;
    auto result_jump = new_index_jump_shape(4, result_num);
    size_t result_sum = result_jump[0] * result_num[0];
    memset(result, 0, n * tx * ty * 3 * sizeof(uint8_t));

    std::unique_ptr<size_t[]> result_average_num = std::make_unique<size_t[]>(2);
    result_average_num[0] = n;
    result_average_num[1] = 3;
    auto result_average_jump = new_index_jump_shape(2, result_average_num);
    size_t result_average_sum = result_average_jump[0] * result_average_num[0];
    std::unique_ptr<uint8_t[]> result_average = std::make_unique<uint8_t[]>(n * 3);
    memset(result_average.get(), 0, n * 3 * sizeof(uint8_t));

    std::unique_ptr<size_t[]> result_dsq2_num = std::make_unique<size_t[]>(2);
    result_dsq2_num[0] = n;
    result_dsq2_num[1] = 3;
    auto result_dsq2_jump = new_index_jump_shape(2, result_dsq2_num);
    size_t result_dsq2_sum = result_dsq2_jump[0] * result_dsq2_num[0];
    std::unique_ptr<double[]> result_dsq2 = std::make_unique<double[]>(n * 3);
    memset(result_dsq2.get(), 0, n * 3 * sizeof(double));

    std::unique_ptr<size_t[]> result_dn_num = std::make_unique<size_t[]>(2);
    result_dn_num[0] = n;
    result_dn_num[1] = 3;
    auto result_dn_jump = new_index_jump_shape(2, result_dn_num);
    size_t result_dn_sum = result_dn_jump[0] * result_dn_num[0];
    std::unique_ptr<size_t[]> result_dn = std::make_unique<size_t[]>(n * 3);
    memset(result_dn.get(), 0, n * 3 * sizeof(size_t));

    std::unique_ptr<size_t[]> image_belong_num = std::make_unique<size_t[]>(2);
    image_belong_num[0] = ix;
    image_belong_num[1] = iy;
    auto image_belong_jump = new_index_jump_shape(2, image_belong_num);
    std::unique_ptr<size_t[]> image_belong = std::make_unique<size_t[]>(ix * iy);
    memset(image_belong.get(), 0, ix * iy * sizeof(size_t));
    size_t image_belong_sum = image_belong_jump[0] * image_belong_num[0];

    size_t image_index = 0, result_index = 0, result_ave_index = 0, image_belong_index = 0;
    size_t result_dsq2_index = 0;


    double ttile = static_cast<double>(tx * ty);
    double ixy = static_cast<double>(ix * iy);

    size_t image_ave_index_100 = image_sum / 100, ii_100_now = 1;

    if (isverbose){
        std::cout << "tilesetauto average: k-mean prosess..." << "" << std::endl;
    }

    if (isverbose){
        std::cout << "tilesetauto average: result initialization..." << "" << std::endl;
    }

    std::srand(static_cast<unsigned int>(rand_seed));
    std::unordered_set<uint32_t> RGB_exist;
    result_ave_index = 0;
    uint32_t RGB_c_temp;
    for (size_t ts = 0 ; ts < n ; ++ts, result_ave_index += result_average_jump[0]){
        for (size_t rgb = 0 ; rgb < 3 ; ++rgb, result_ave_index += result_average_jump[1]){
            check_leak(result_ave_index, result_average_sum);
            result_average[result_ave_index] = std::rand();
        }
        
        result_ave_index -= result_average_jump[0];

        RGB_c_temp = (static_cast<uint32_t>(result_average[result_ave_index]) << 16) + \
                        (static_cast<uint32_t>(result_average[result_ave_index + 1]) << 8) + \
                        (static_cast<uint32_t>(result_average[result_ave_index + 2]));
        if (RGB_exist.find(RGB_c_temp) != RGB_exist.end()){
            result_ave_index -= result_average_jump[0];
            --ts;
        }
        else{
            RGB_exist.insert(RGB_c_temp);
        }
    }


    double dis_temp;
    size_t belong_to_s;
    ii_100_now = 0;
    bool end_cycle = true;
    uint8_t result_temp;
    int32_t result_sub = std::numeric_limits<int32_t>::max(), result_sub_temp;
    while (ii_100_now < limit_cycle && result_sub > stopnum){

        if (isverbose){
            if (ii_100_now == 0){
                std::cout << "tilesetauto average: k-mean " << ii_100_now << " round..." << std::endl;
            }
            else{
                std::cout << "tilesetauto average: k-mean " << ii_100_now << " rounds...(move_sum: " << result_sub << ")(->" << stopnum << ", end)" << std::endl;
            }
        }

        image_index = 0, image_belong_index = 0; 
        for (size_t ixn = 0 ; ixn < ix ; ++ixn, image_index += image_jump[0], image_belong_index += image_belong_jump[0]){
            
            for (size_t iyn = 0 ; iyn < iy ; ++iyn, image_index += image_jump[1], image_belong_index += image_belong_jump[1]){

                double min_dis = DBL_MAX;

                
                result_ave_index = 0;
                for (size_t ts = 0 ; ts < n ; ++ts, result_ave_index += result_average_jump[0]){
                    check_leak(image_index + 2, image_sum);
                    check_leak(result_ave_index + 2, result_average_sum);
                    dis_temp = sRGB_square2(image + image_index, result_average.get() + result_ave_index);

                    if (dis_temp < min_dis){
                        min_dis = dis_temp;
                        belong_to_s = ts * result_average_jump[0];
                    }
                }
                /*
                if (ii_100_now == 20 && (ixn % 355 == 0) && (iyn % 355 == 0)){
                    pi("coodinate:");
                    pi(static_cast<int>(ixn));
                    pi(static_cast<int>(iyn));
                    pi("result:");
                    pi(static_cast<int>(result_average[result_ave_index - result_average_sum + belong_to_s]));
                    pi(static_cast<int>(result_average[result_ave_index - result_average_sum + belong_to_s + 1]));
                    pi(static_cast<int>(result_average[result_ave_index - result_average_sum + belong_to_s + 2]));
                    pi("image:");
                    pi(static_cast<int>(image[image_index]));
                    pi(static_cast<int>(image[image_index + 1]));
                    pi(static_cast<int>(image[image_index + 2]));
                    petr("");
                }*/
                check_leak(image_belong_index, image_belong_sum);
                image_belong[image_belong_index] = belong_to_s;

            }
            image_index -= image_jump[0];
            image_belong_index -= image_belong_jump[0];
        }

        image_index = 0, image_belong_index = 0; 
        memset(result_dsq2.get(), 0, n * 3 * sizeof(double));
        memset(result_dn.get(), 0, n * 3 * sizeof(size_t));
        size_t image_belong_temp;
        for (size_t ixn = 0 ; ixn < ix ; ++ixn, image_index += image_jump[0], image_belong_index += image_belong_jump[0]){

            for (size_t iyn = 0 ; iyn < iy ; ++iyn, image_index += image_jump[1], image_belong_index += image_belong_jump[1]){

                check_leak(image_belong_index, image_belong_sum);
                image_belong_temp = image_belong[image_belong_index];
                for (size_t rgb = 0 ; rgb < 3 ; ++rgb, image_index += image_jump[2]){
                    
                    check_leak(image_index, image_sum);
                    check_leak(image_belong_temp, result_dsq2_sum);
                    check_leak(image_belong_temp, result_dn_sum);
                    result_dsq2[image_belong_temp + rgb] += image[image_index];
                    ++result_dn[image_belong_temp + rgb];
                }
                image_index -= image_jump[1];

            }
            image_index -= image_jump[0];
            image_belong_index -= image_belong_jump[0];
        }

        result_ave_index = 0, result_dsq2_index = 0;
        result_sub = 0;
        RGB_exist.clear();
        for (size_t ts = 0 ; ts < n ; ++ts, result_ave_index += result_average_jump[0], result_dsq2_index += result_dsq2_jump[0]){

            for (size_t rgb = 0 ; rgb < 3 ; ++rgb, result_ave_index += result_average_jump[1], result_dsq2_index += result_dsq2_jump[1]){
                
                check_leak(result_ave_index, result_average_sum);
                check_leak(image_belong_temp, result_dsq2_sum);
                check_leak(image_belong_temp, result_dn_sum);
                if (result_dn[result_dsq2_index] == 0){
                    result_temp = std::rand();
                }
                else{
                    result_temp = static_cast<uint8_t>(result_dsq2[result_dsq2_index] / result_dn[result_dsq2_index]);
                }

                if (result_average[result_ave_index] != result_temp){
                    result_sub_temp = static_cast<int32_t>(result_temp) - result_average[result_ave_index];
                    result_sub += std::abs(result_sub_temp);
                    result_average[result_ave_index] = result_temp;
                }
            }

            result_ave_index -= result_average_jump[0];
            result_dsq2_index -= result_dsq2_jump[0];
            
            check_leak(result_ave_index + 2, result_average_sum);
            RGB_c_temp = (static_cast<uint32_t>(result_average[result_ave_index]) << 16) + \
                        (static_cast<uint32_t>(result_average[result_ave_index + 1]) << 8) + \
                        (static_cast<uint32_t>(result_average[result_ave_index + 2]));

            if (RGB_exist.find(RGB_c_temp) != RGB_exist.end()){
                result_dsq2_index -= result_dsq2_jump[0];
                result_ave_index -= result_average_jump[0];
                --ts;
            }
            else{
                RGB_exist.insert(RGB_c_temp);
            }

            /*
            if (pin[0] + pin[1] + pin[2] != 0){
                for (size_t rgb = 0 ; rgb < 3 ; ++rgb){
                    pi(pin[rgb]);
                }
                petr("");
            }*/


        }
        //petr("");
        ++ii_100_now;
    }

    if (isverbose){
        std::cout << "tilesetauto average: k-mean prosess complete..." << std::endl;
    }

    if (isverbose){
        std::cout << "tilesetauto average: tile rearrangement..." << std::endl;
    }

    std::unique_ptr<RGB[]> result_rgb = std::make_unique<RGB[]>(n);

    result_ave_index = 0;
    for (size_t ts = 0 ; ts < n ; ++ts, result_ave_index += result_average_jump[0]){
        
        check_leak(ts, n);
        check_leak(result_ave_index + 2, result_average_sum);
        result_rgb[ts].r = result_average[result_ave_index];
        result_rgb[ts].g = result_average[result_ave_index + 1];
        result_rgb[ts].b = result_average[result_ave_index + 2];
    }

    std::unique_ptr<HSV[]> result_hsv = std::make_unique<HSV[]>(n);

    for (size_t ts = 0 ; ts < n ; ++ts){
        check_leak(ts, n);
        result_hsv[ts] = RGBtoHSV(result_rgb[ts]);
        result_hsv[ts].oi = ts * 3;
    }

    std::sort(result_hsv.get(), result_hsv.get() + n, &HSV_compare_S_b);

    size_t ths = n;
    for (size_t ts = 0 ; ts < n ; ++ts){

        check_leak(ts, n);
        if (result_hsv[ts].s < threshold_S){
            ths = ts;
            break;
        }
    }
    check_leak(ths - 1, n);

    std::sort(result_hsv.get(), result_hsv.get() + ths, &HSV_compare_V_b);

    for (size_t ts = 0 ; ts < ths ; ++ts){

        check_leak(ts, n);
        if (result_hsv[ts].v < threshold_V){
            ths = ts;
            break;
        }
    }

    ths = (ths / ny) * ny;
    //pi("ths:");
    //petr(ths);

    if (ths != 0){
        check_leak(ths, n);

        std::sort(result_hsv.get(), result_hsv.get() + ths, &HSV_compare_H);
        size_t index_maxsub = 0;
        double biggest_HSVh_subabs = (result_hsv[0].h + 360 - result_hsv[ths - 1].h);
        
        for (size_t ts = 1 ; ts < ths ; ++ts){
            if (result_hsv[ts].h > 300){
                check_leak(ts - 1, n);
                check_leak(ts, n);
                double subtemp = result_hsv[ts].h - result_hsv[ts - 1].h;
                if (subtemp > biggest_HSVh_subabs){
                    index_maxsub = ts;
                    biggest_HSVh_subabs = subtemp;
                }
            }
        }

        std::unique_ptr<HSV[]> result_hsv_t = std::make_unique<HSV[]>(ths);

        for (size_t ts = 0 ; ts < ths ; ++ts){
            
            check_leak(ts, ths);
            result_hsv_t[ts] = result_hsv[ts];
        }

        for (size_t ts = 0 ; ts < ths ; ++ts){
            check_leak(ts, n);
            check_leak((ts + (ths - index_maxsub)) % ths, ths);
            result_hsv[ts] = result_hsv_t[(ts + (ths - index_maxsub)) % ths];
        }

        for (size_t ts = 0 ; ts < ths ; ts += ny){

            check_leak(ts + ny - 1, n);

            std::sort(result_hsv.get() + ts, result_hsv.get() + ts + ny, &HSV_compare_SV);
        }

    }

    std::sort(result_hsv.get() + ths, result_hsv.get() + n, &HSV_compare_V_b);

    for (size_t ts = ths ; ts < n ; ts += ny){
        check_leak(ts + ny - 1, n);
        std::sort(result_hsv.get() + ts, result_hsv.get() + ts + ny, &HSV_compare_S);
    }

    std::unique_ptr<uint8_t[]> result_average_t = std::make_unique<uint8_t[]>(n * 3);

    result_ave_index = 0;
    for (size_t ts = 0 ; ts < n ; ++ts, result_ave_index += result_average_jump[0]){
        for (size_t rgb = 0 ; rgb < 3 ; ++rgb){
            check_leak(result_ave_index + 2, result_average_sum);
            result_average_t[result_ave_index + rgb] = result_average[result_ave_index + rgb];
        }
    }

    result_ave_index = 0;
    //petr("sort_to:");
    for (size_t ts = 0 ; ts < n ; ++ts, result_ave_index += result_average_jump[0]){
        
        //pi(result_hsv[ts].oi);

        //if (ts % ny == ny - 1){
        //    petr("");
        //}

        for (size_t rgb = 0 ; rgb < 3 ; ++rgb){
            check_leak(result_ave_index + 2, result_average_sum);
            check_leak(result_hsv[ts].oi + rgb, result_average_sum);
            result_average[result_ave_index + rgb] = result_average_t[result_hsv[ts].oi + rgb];
        }
    }

    if (isverbose){
        result_ave_index = 0;
        std::cout << "tilesetauto average: rgb outputting..." << std::endl;
        for (size_t ts = 0 ; ts < n ; ++ts, result_ave_index += result_average_jump[0]){
            if (ts % ny == 0){
                if (ts != 0) std::cout << std::endl;
            }
            else{
                std::cout << ", ";
            }
            print_rgb(result_average.get() + result_ave_index);
        }
        std::cout << std::endl;
    }

    result_ave_index = 0, result_index = 0;
    for (size_t ts = 0 ; ts < n ; ++ts, result_ave_index += result_average_jump[0], result_index += result_jump[0]){
        for (size_t txn = 0 ; txn < tx ; ++txn, result_index += result_jump[1]){
            for (size_t tyn = 0 ; tyn < ty ; ++tyn, result_index += result_jump[2]){
                for (size_t rgb = 0 ; rgb < 3 ; ++rgb, result_ave_index += result_average_jump[1], result_index += result_jump[3]){
                    
                    check_leak(result_index, result_sum);
                    result[result_index] = result_average[result_ave_index];
                }
                result_ave_index -= result_average_jump[0];
                result_index -= result_jump[2];
            }
            result_index -= result_jump[1];
        }
        result_index -= result_jump[0];
    }

    if (isverbose){
        std::cout << "tilesetauto average has been processed." << std::endl;
    }
    return;
}

py::array_t<uint8_t> tilesetauto(py::array_t<uint8_t> image, py::array_t<uint32_t> tileset_size, int mode_code, int stopnum = 0, int rand_seed = -1, int limit_cycle = -1, bool isverbose = false, bool isdebug = false) {
    
    if (isverbose){
        std::cout << "tilesetauto: initialization..." << std::endl;
    }

    // must be memory continuous, please do np.ascontiguousarray() first.
    // must deepcopy(from python) or be sure that the argument would not use(in python). 

    // image : dim(3), (ix iy 3), RGB matrix | (ix, iy)
    // tileset_size : dim(1), (4), (nx, ny, tx, ty)
    // mode_code : int, {0: average mode, }
    // rand_seed : int, -1(time as seed), or qualified seed
    // limit_cycle : int, -1(max cycle of k-mean), or 16 * nx * ny
    // stopnum : int, 0(move number when stopping(k-mean))

    // result : dim(4), (n, tx, ty, 3)

    const py::ssize_t* image_shape = image.shape();
    py::ssize_t image_dim = image.ndim();
    const py::ssize_t ix = image_shape[0];
    const py::ssize_t iy = image_shape[1];

    const py::ssize_t* tileset_size_shape = tileset_size.shape();
    py::ssize_t tileset_size_dim = tileset_size.ndim();
    py::ssize_t nx = static_cast<py::ssize_t>(tileset_size.at(0));
    py::ssize_t ny = static_cast<py::ssize_t>(tileset_size.at(1));
    py::ssize_t tx = static_cast<py::ssize_t>(tileset_size.at(2));
    py::ssize_t ty = static_cast<py::ssize_t>(tileset_size.at(3));
    py::ssize_t n = nx * ny;

    std::vector<py::ssize_t> result_shape = {n, tx, ty, 3};
    py::array_t<uint8_t> result(result_shape);

    uint8_t* image_ptr = static_cast<uint8_t*>(image.request().ptr);
    uint8_t* result_ptr = static_cast<uint8_t*>(result.request().ptr);

    std::array<ptrdiff_t, 3> image_shape_n = {ix, iy, 3};
    std::array<ptrdiff_t, 1> tileset_size_shape_n = {4};

    runtime_error_s<const py::ssize_t, ptrdiff_t>("tilesetauto : image", 3, image_dim, image_shape, image_shape_n.data());
    runtime_error_s<const py::ssize_t, ptrdiff_t>("tilesetauto : tileset_size", 1, tileset_size_dim, tileset_size_shape, tileset_size_shape_n.data());

    if (isverbose){
        std::cout << "tilesetauto mode: process..." << std::endl;
        std::cout << "    image:(" << ix << "," << iy << "," << 3 << ")" << std::endl;
        std::cout << "    tileset_size:(" << nx << "," << ny << "," << tx << "," << ty << "," << 3 << ")" << std::endl;
        std::cout << "    stopnum:" << stopnum << ",mode_code:" << mode_code << ",limit_cycle:" << limit_cycle << ",rand_seed:" << rand_seed << ",ix:" << ix << ",iy:" << iy << ",tx:" << tx << ",ty:" << ty << ",n:" << n << std::endl;
    }

    std::time_t real_rand_seed;
    if (rand_seed <= -1){
        real_rand_seed = std::time(nullptr);
    }
    else{
        real_rand_seed = rand_seed;
    }

    size_t real_limit_cycle;
    if (limit_cycle <= -1){
        real_limit_cycle = 16 * n;
    }
    else{
        real_limit_cycle = limit_cycle;
    }

    switch (mode_code){
        case 0:
            tilesetauto_average(image_ptr, result_ptr, n, ny, ix, iy, tx, ty, stopnum, real_rand_seed, real_limit_cycle, mode_code, isverbose = isverbose, isdebug = isdebug);
            break;
        default:
            throw std::runtime_error("tilesetauto : mode code error");
    }

    if (isverbose){
        std::cout << "tilesetauto has been processed." << std::endl;
    }

    return result;
}

void bind_module_tilesetauto(py::module_& m) {
    m.def("tilesetauto", &tilesetauto, "Automatically add tilesets");
}