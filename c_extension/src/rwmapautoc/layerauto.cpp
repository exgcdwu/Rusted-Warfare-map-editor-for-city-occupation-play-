#include <vector>
#include <cstdint>
#include <memory>
#include <cfloat>
#include <string>
#include <cstring>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
namespace py = pybind11;

#include "CIE2000.hpp"
#include "utility.hpp"
#include "rwmapautoc_core.hpp"

int add(int i, int j){
    return i + j;
}

py::array_t<double> matrix_mul(py::array_t<double> a, py::array_t<double> b) {

    const py::ssize_t* a_shape = a.shape();
    py::ssize_t a_dim = a.ndim();
    const py::ssize_t* b_shape = b.shape();
    py::ssize_t b_dim = b.ndim();

    if (a_dim != 2 || b_dim != 2 || a_shape[1] != b_shape[0]) {
        throw std::runtime_error("Incompatible matrix dimensions for multiplication");
    }

    std::vector<py::ssize_t> result_shape = {a_shape[0], b_shape[1]};

    py::array_t<double> result(result_shape);

    auto a_buf = a.request(), b_buf = b.request(), r_buf = result.request();
    double* a_ptr = static_cast<double*>(a_buf.ptr);
    double* b_ptr = static_cast<double*>(b_buf.ptr);
    double* r_ptr = static_cast<double*>(r_buf.ptr);

    for (py::ssize_t i = 0; i < a_shape[0]; i++) {
        for (py::ssize_t j = 0; j < b_shape[1]; j++) {
            double sum = 0;
            for (py::ssize_t k = 0; k < a_shape[1]; k++) {
                sum += a_ptr[i * a_shape[1] + k] * b_ptr[k * b_shape[1] + j];
            }
            r_ptr[i * b_shape[1] + j] = sum;
        }
    }

    return result;
}

void layerauto_throw_index(size_t image_ave_index, size_t image_index, size_t result_index,
                          size_t tileset_index, size_t tileset_ave_index, size_t image_average_sum, 
                          size_t image_sum, size_t result_sum, size_t tileset_sum, 
                          size_t tileset_average_sum){
                            throw_index(image_ave_index, image_average_sum, 0);
                            throw_index(image_index, image_sum, 1);
                            throw_index(result_index, result_sum, 2);
                            throw_index(tileset_index, tileset_sum, 3);
                            throw_index(tileset_ave_index, tileset_average_sum, 4);
                          }

void layerauto_average(uint8_t* image, uint8_t* tileset, uint32_t* tileset_gid, uint32_t* result, const size_t n, const size_t ix, const size_t iy, const size_t tx, const size_t ty, const int mode_code, bool isverbose = false, bool isdebug = false){
    if (isverbose){
        std::cout << "layerauto average mode: process..." << std::endl;
        std::cout << "    image:(" << ix * tx << "," << iy * ty << "," << 3 << ")" << std::endl;
        std::cout << "    tileset:(" << n << "," << tx << "," << ty << "," << 3 << ")" << std::endl;
        std::cout << "    tileset_index:(" << n << ")" << std::endl;
        std::cout << "    layer:(" << ix << "," << iy << ")" << std::endl;
        std::cout << "    mode:(" << mode_code << ",ix:" << ix << ",iy:" << iy << ",tx:" << tx << ",ty:" << ty << ",n:" << n << std::endl;
    }

    if (isverbose){
        std::cout << "layerauto average: initialization..." << std::endl;
    }

    std::unique_ptr<size_t[]> image_num = std::make_unique<size_t[]>(5);
    image_num[0] = ix;
    image_num[1] = tx;
    image_num[2] = iy;
    image_num[3] = ty;
    image_num[4] = 3;
    auto image_jump = new_index_jump_shape(5, image_num);
    size_t image_sum = image_jump[0] * image_num[0];

    std::unique_ptr<size_t[]> tileset_num = std::make_unique<size_t[]>(4);
    tileset_num[0] = n;
    tileset_num[1] = tx;
    tileset_num[2] = ty;
    tileset_num[3] = 3;
    auto tileset_jump = new_index_jump_shape(4, tileset_num);
    size_t tileset_sum = tileset_jump[0] * tileset_num[0];

    std::unique_ptr<size_t[]> result_num = std::make_unique<size_t[]>(2);
    result_num[0] = ix;
    result_num[1] = iy;
    auto result_jump = new_index_jump_shape(2, result_num);
    size_t result_sum = result_jump[0] * result_num[0];
    memset(result, 0, ix * iy * sizeof(uint32_t));

    std::unique_ptr<size_t[]> tileset_average_num = std::make_unique<size_t[]>(2);
    tileset_average_num[0] = n;
    tileset_average_num[1] = 3;
    auto tileset_average_jump = new_index_jump_shape(2, tileset_average_num);
    std::unique_ptr<double[]> tileset_average = std::make_unique<double[]>(n * 3);
    memset(tileset_average.get(), 0, n * 3 * sizeof(double));
    size_t tileset_average_sum = tileset_average_jump[0] * tileset_average_num[0];

    std::unique_ptr<size_t[]> image_average_num = std::make_unique<size_t[]>(3);
    image_average_num[0] = ix;
    image_average_num[1] = iy;
    image_average_num[2] = 3;
    auto image_average_jump = new_index_jump_shape(3, image_average_num);
    std::unique_ptr<double[]> image_average = std::make_unique<double[]>(ix * iy * 3);
    memset(image_average.get(), 0, ix * iy * 3 * sizeof(double));
    size_t image_average_sum = image_average_jump[0] * image_average_num[0];

    size_t image_ave_index = 0, image_index = 0, result_index = 0;
    size_t tileset_index = 0, tileset_ave_index = 0;

    double ttile = static_cast<double>(tx * ty);

    if (isverbose){
        std::cout << "layerauto average: tileset process...(" << tx * ty * n * 3 << ")" << std::endl;
    }


    for (size_t ts = 0 ; ts < n ; ++ts, tileset_index += tileset_jump[0], tileset_ave_index += tileset_average_jump[0]){
        for (size_t txn = 0 ; txn < tx ; ++txn, tileset_index += tileset_jump[1]){
            for (size_t tyn = 0 ; tyn < ty ; ++tyn, tileset_index += tileset_jump[2]){
                for (size_t rgb = 0 ; rgb < 3 ; ++rgb, tileset_index += tileset_jump[3], tileset_ave_index += tileset_average_jump[1]){
                    tileset_average[tileset_ave_index] += tileset[tileset_index];
                    if (isdebug){
                        layerauto_throw_index(image_ave_index, image_index, result_index, tileset_index, tileset_ave_index, 
                                        image_average_sum, image_sum, result_sum, tileset_sum, tileset_average_sum);
                    }
                }
                tileset_index -= tileset_jump[2];
                tileset_ave_index -= tileset_average_jump[0];
            }
            tileset_index -= tileset_jump[1];
        }

        tileset_index -= tileset_jump[0];

        for (size_t rgb = 0 ; rgb < 3 ; ++rgb, tileset_ave_index += tileset_average_jump[1]){
            tileset_average[tileset_ave_index] /= ttile;
        }
        tileset_ave_index -= tileset_average_jump[0];
    }
    tileset_index = 0;
    tileset_ave_index = 0;

    size_t image_ave_index_100 = image_average_sum / 100, ii_100_now = 1;

    if (isverbose){
        std::cout << "layerauto average: image prosess...(" << ix * iy * 3 << ")" << std::endl;
    }


    for (size_t ixn = 0 ; ixn < ix ; ++ixn, image_index += image_jump[0], image_ave_index += image_average_jump[0]){

        for (size_t iyn = 0 ; iyn < iy ; ++iyn, image_index += image_jump[2], image_ave_index += image_average_jump[1]){    

            for (size_t rgb = 0 ; rgb < 3 ; ++rgb, image_index += image_jump[4], image_ave_index += image_average_jump[2]){

                for (size_t txn = 0 ; txn < tx ; ++txn, image_index += image_jump[1]){

                    for (size_t tyn = 0 ; tyn < ty ; ++tyn, image_index += image_jump[3]){

                        image_average[image_ave_index] += image[image_index];
                    }
                    image_index -= image_jump[2];
                }
                image_index -= image_jump[0];
                image_average[image_ave_index] /= ttile;
            }
            image_index -= image_jump[3], image_ave_index -= image_average_jump[1];


            if (isverbose && ((image_ave_index / image_ave_index_100) == ii_100_now)){
                std::cout << "    layerauto average: image prosess (" << image_ave_index << "/" << image_average_sum << ")" << std::to_string(ii_100_now) << "%..." << std::endl;
                ii_100_now += (ii_100_now / 3) + 1;
            }
        }
        image_index -= image_jump[1], image_ave_index -= image_average_jump[0];
    }

    if (isverbose){
        std::cout << "layerauto average: image prosess complete..." << std::endl;
    }

    if (isverbose){
        std::cout << "layerauto average: layer prosess...(" << ix * iy * 3 << ")" << std::endl;
    }

    image_index = 0, image_ave_index = 0, tileset_ave_index = 0, result_index = 0;
    ii_100_now = 1;
    for (size_t ixn = 0 ; ixn < ix ; ++ixn, image_ave_index += image_average_jump[0], result_index += result_jump[0]){

        for (size_t iyn = 0 ; iyn < iy ; ++iyn, image_ave_index += image_average_jump[1], result_index += result_jump[1]){

            double min_CIE2000 = DBL_MAX;
            uint32_t gid_now = 0;
            double image_ave_temp[3], tileset_ave_temp[3];
            for (size_t ts = 0 ; ts < n ; ++ts, tileset_ave_index += tileset_average_jump[0]){
                
                for (size_t rgb = 0 ; rgb < 3 ; ++rgb, image_ave_index += image_average_jump[2], tileset_ave_index += tileset_average_jump[1]){

                    if (isdebug){
                        layerauto_throw_index(image_ave_index, image_index, result_index, tileset_index, tileset_ave_index, 
                                        image_average_sum, image_sum, result_sum, tileset_sum, tileset_average_sum);
                    }

                    image_ave_temp[rgb] = image_average[image_ave_index];
                    tileset_ave_temp[rgb] = tileset_average[tileset_ave_index];
                }

                tileset_ave_index -= tileset_average_jump[0];
                image_ave_index -= image_average_jump[1];
                
                double CIE_now;

                switch (mode_code){
                    case 0:
                        CIE_now = sRGB_square2(image_ave_temp, tileset_ave_temp);
                        break;
                    case 1:
                        CIE_now = sRGB_to_CIE2000(image_ave_temp, tileset_ave_temp);
                        break;
                    default:
                        throw std::runtime_error("layerauto average: mode code error");
                }

                if (min_CIE2000 > CIE_now){
                    min_CIE2000 = CIE_now;
                    gid_now = tileset_gid[ts];
                }

            }
            tileset_ave_index = 0;

            result[result_index] = gid_now;

            if (isverbose && ((image_ave_index / image_ave_index_100) == ii_100_now)){
                std::cout << "    layerauto average: layer prosess (" << image_ave_index << "/" << image_average_sum << ")" << std::to_string(ii_100_now) << "%..." << std::endl;
                ii_100_now += (ii_100_now / 3) + 1;
            }
        }
        image_ave_index -= image_average_jump[0], result_index -= result_jump[0];
    }

    if (isverbose){
        std::cout << "layerauto average: layer prosess complete..." << std::endl;
    }

    if (isverbose){
        std::cout << "layerauto average has been processed." << std::endl;
    }
    return;


}

py::array_t<uint32_t> layerauto(py::array_t<uint8_t> image, py::array_t<uint8_t> tileset, py::array_t<uint32_t> tileset_index, int mode_code, bool isverbose = false, bool isdebug = false) {
    
    if (isverbose){
        std::cout << "layerauto: initialization..." << std::endl;
    }

    // must be memory continuous, please do np.ascontiguousarray() first.
    // must deepcopy(from python) or be sure that the argument would not use(in python). 

    // image : dim(3), (ix * tx iy * ty 3), RGB matrix | (ix | tx, iy | ty)
    // tileset : dim(4), (n tx ty 3), RGB matrix
    // tileset_index : dim(1), (n), index array
    // tile_size : dim(1), (2), (tx, ty)
    // mode_code : int, {0: average square mode, 1 average CIE2000 mode, 2 corner terrain mode, 3 adj terrain mode, 4 mix terrain mode}
    // tileset_terrain : dim(2) (n, 4/8) the terrain of every tile(4:corner, adj;8: mix)

    // result : dim(2), (ix / tx, iy / ty)

    const py::ssize_t* image_shape = image.shape();
    py::ssize_t image_dim = image.ndim();
    const py::ssize_t ixt = image_shape[0];
    const py::ssize_t iyt = image_shape[1];

    const py::ssize_t* tileset_shape = tileset.shape();
    py::ssize_t tileset_dim = tileset.ndim();
    const py::ssize_t n = tileset_shape[0];
    const py::ssize_t tx = tileset_shape[1];
    const py::ssize_t ty = tileset_shape[2];
    const py::ssize_t ix = ixt / tx;
    const py::ssize_t iy = iyt / ty;

    const py::ssize_t* tileset_index_shape = tileset_index.shape();
    py::ssize_t tileset_index_dim = tileset_index.ndim();

    std::vector<py::ssize_t> result_shape = {ix, iy};
    py::array_t<uint32_t> result(result_shape);

    uint8_t* image_ptr = static_cast<uint8_t*>(image.request().ptr);
    uint8_t* tileset_ptr = static_cast<uint8_t*>(tileset.request().ptr);
    uint32_t* tileset_index_ptr = static_cast<uint32_t*>(tileset_index.request().ptr);
    uint32_t* result_ptr = static_cast<uint32_t*>(result.request().ptr);

    std::array<ptrdiff_t, 3> image_shape_n = {ixt, iyt, 3};
    std::array<ptrdiff_t, 4> tileset_shape_n = {n, tx, ty, 3};
    std::array<ptrdiff_t, 1> tileset_index_shape_n = {n};
    std::array<ptrdiff_t, 1> tile_size_shape_n = {2};

    runtime_error_s<const py::ssize_t, ptrdiff_t>("layerauto : image", 3, image_dim, image_shape, image_shape_n.data());
    runtime_error_s<const py::ssize_t, ptrdiff_t>("layerauto : tileset", 4, tileset_dim, tileset_shape, tileset_shape_n.data());
    runtime_error_s<const py::ssize_t, ptrdiff_t>("layerauto : tileset_index", 1, tileset_index_dim, tileset_index_shape, tileset_index_shape_n.data());

    if (ixt % tx != 0 || iyt % ty != 0) {
        throw std::runtime_error("layerauto : error(image shape truediv error)");
    }

    if (isverbose){
        std::cout << "layerauto mode: process..." << std::endl;
        std::cout << "    image:(" << ix * tx << "," << iy * ty << "," << 3 << ")" << std::endl;
        std::cout << "    tileset:(" << n << "," << tx << "," << ty << "," << 3 << ")" << std::endl;
        std::cout << "    tileset_index:(" << n << ")" << std::endl;
        std::cout << "    layer:(" << ix << "," << iy << ")" << std::endl;
        std::cout << "    ix:" << ix << ",iy:" << iy << ",tx:" << tx << ",ty:" << ty << ",n:" << n << std::endl;
    }

    switch (mode_code){
        case 0:
            layerauto_average(image_ptr, tileset_ptr, tileset_index_ptr, result_ptr, n, ix, iy, tx, ty, mode_code, isverbose, isdebug);
            break;
        case 1:
            layerauto_average(image_ptr, tileset_ptr, tileset_index_ptr, result_ptr, n, ix, iy, tx, ty, mode_code, isverbose, isdebug);
            break;
        default:
            throw std::runtime_error("layerauto : mode code error");
    }

    if (isverbose){
        std::cout << "layerauto has been processed." << std::endl;
    }

    return result;
}

void bind_module_layerauto(py::module_& m) {
    m.def("add", &add, "A function which adds two numbers");
    m.def("layerauto", &layerauto, "Automatically add tiles");
    m.def("matrix_mul", &matrix_mul, "Matrix multiplication");
}