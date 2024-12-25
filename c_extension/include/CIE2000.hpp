#ifndef CIE2000_HPP

#define CIE2000_HPP

    #define M_PI 3.14159265358979323846

    // D65 reference white
    const double Xr = 95.047;
     const double Yr = 100.000;
     const double Zr = 108.883;

    // CIE_gamma
     const double CIE_gamma = 2.4;

    // CIE2000 arguments
     const double kL = 0.015;
     const double kC = 0.045;
     const double kH = 0.015;



      std::array<double, 3> sRGB_to_XYZ(double*);
      std::array<double, 3> XYZ_to_LAB(std::array<double, 3>&);
      std::array<double, 3> sRGB_to_LAB(double*);
      double LAB_to_CIE2000(std::array<double, 3>& Lab1, std::array<double, 3>&);
      double sRGB_to_CIE2000(double*, double*);


#endif // CIE2000_HPP