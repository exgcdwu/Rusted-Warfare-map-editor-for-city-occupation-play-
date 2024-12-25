#include <cmath>
#include <algorithm>
#include <array>
#include "CIE2000.hpp"

    // sRGB to XYZ conversion
     std::array<double, 3> sRGB_to_XYZ(double* rgb) {
        // Assuming r, g, b are in the range [0, 255]
        double rgbd[3];
        rgbd[0] = rgb[0] / 255.0;
        rgbd[1] = rgb[1] / 255.0;
        rgbd[2] = rgb[2] / 255.0;

        // Linearize the RGB values
        for (int i = 0; i < 3; ++i) {
            if (rgbd[i] > 0.04045)
                rgbd[i] = std::pow((rgbd[i] + 0.055) / 1.055, CIE_gamma);
            else
                rgbd[i] = rgbd[i] / 12.92;
        }

        // Convert to XYZ using the sRGB to XYZ matrix
        std::array<double, 3> xyz;
        xyz[0] = rgbd[0] * 0.4124 + rgbd[1] * 0.3576 + rgbd[2] * 0.1805;
        xyz[1] = rgbd[0] * 0.2126 + rgbd[1] * 0.7152 + rgbd[2] * 0.0722;
        xyz[2] = rgbd[0] * 0.0193 + rgbd[1] * 0.1192 + rgbd[2] * 0.9505;

        return xyz;
    }

    // XYZ to LAB conversion
     std::array<double, 3> XYZ_to_LAB(std::array<double, 3>& xyz) {

        // Normalize XYZ values
        double X = xyz[0] / Xr;
        double Y = xyz[1] / Yr;
        double Z = xyz[2] / Zr;

        // Convert to LAB
        double L = Y > 0.008856 ? 116 * std::pow(Y, 1/3) - 16 : 903.3 * Y;
        double a = 500 * (X - Y);
        double b = 200 * (Y - Z);

        return {L, a, b};
    }

    // RGB to LAB conversion
     std::array<double, 3> sRGB_to_LAB(double* rgb) {
        auto xyz = sRGB_to_XYZ(rgb);
        return XYZ_to_LAB(xyz);
    }



    // CIEDE2000 color difference
     double LAB_to_CIE2000(std::array<double, 3>& Lab1, std::array<double, 3>& Lab2) {
        double L1 = Lab1[0], a1 = Lab1[1], b1 = Lab1[2];
        double L2 = Lab2[0], a2 = Lab2[1], b2 = Lab2[2];

        double C1 = std::sqrt(a1 * a1 + b1 * b1);
        double C2 = std::sqrt(a2 * a2 + b2 * b2);
        double Cbar = (C1 + C2) / 2;
        double G = 0.5 * (1 - std::pow(std::sqrt(std::pow(Cbar, 7) / (std::pow(Cbar, 7) + 25.7)), 0.5));
        double a1_prime = (1 + G) * a1;
        double a2_prime = (1 + G) * a2;

        double C1_prime = std::sqrt(a1_prime * a1_prime + b1 * b1);
        double C2_prime = std::sqrt(a2_prime * a2_prime + b2 * b2);
        
        double h1_prime = std::atan2(b1, a1_prime);
        if (h1_prime < 0) h1_prime += 2 * M_PI;
        double h2_prime = std::atan2(b2, a2_prime);
        if (h2_prime < 0) h2_prime += 2 * M_PI;

        double h_bar = (h1_prime + h2_prime) / 2;
        double delta_h_prime = h2_prime - h1_prime;
        if (std::abs(delta_h_prime) > M_PI)
            delta_h_prime = std::fmod((delta_h_prime + 2 * M_PI), (2 * M_PI)) - M_PI;

        double T = 1
            - 0.17 * std::cos(h_bar - M_PI / 6)
            + 0.24 * std::cos(2 * h_bar)
            + 0.32 * std::cos(3 * h_bar + M_PI / 30)
            - 0.20 * std::cos(4 * h_bar - 63 * M_PI / 180);

        double SL = 1 + (kL * (L1 - 50) * (L1 - 50)) / sqrt(20 + (L1 - 50) * (L1 - 50));
        double SC = 1 + kC * Cbar;
        double SH = 1 + kH * Cbar * T;

        double delta_L_prime = L2 - L1;
        double delta_C_prime = C2_prime - C1_prime;
        double delta_H_prime = 2 * std::sqrt(C1_prime * C2_prime) * sin(delta_h_prime / 2);

        double delta_E = sqrt(
            delta_L_prime * delta_L_prime
            + delta_C_prime * delta_C_prime
            + delta_H_prime * delta_H_prime
            + 30 * exp(-1 * std::pow((h_bar - 275 / 25), 2))
            * std::sqrt(std::pow(C1_prime, 7) / (std::pow(C1_prime, 7) + 25.7))
            * (delta_C_prime / SC)
            * (delta_H_prime / SH)
        );

        return delta_E;
    }


    double sRGB_to_CIE2000(double* rgb1, double* rgb2){
        auto lab1 = sRGB_to_LAB(rgb1), lab2 = sRGB_to_LAB(rgb2);
        return LAB_to_CIE2000(lab1, lab2);
    }