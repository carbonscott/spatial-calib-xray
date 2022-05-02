## Past works on the problem

- [power diffraction ring detection](https://www.researchgate.net/profile/Michael-Hart-5/publication/258764497_Weighted_Least_Squares_Fit_of_an_Ellipse_to_Describe_Complete_or_Spotty_Diffraction_Rings_on_a_Planar_2D_Detector/links/55b8838908aec0e5f4399801/Weighted-Least-Squares-Fit-of-an-Ellipse-to-Describe-Complete-or-Spotty-Diffraction-Rings-on-a-Planar-2D-Detector.pdf?origin=publication_detail)


## Environment variables for loading images with `psana`

- `export SIT_PSDM_DATA=/cds/data/drpsrcf`



## Method: Max intensity

- [link](https://scikit-image.org/docs/stable/api/skimage.draw.html#skimage.draw.circle_perimeter)

- Min model: -f(theta)
  - x_i = r * cos(theta_i) + x_0
  - y_i = r * sin(theta_i) + x_0
  - f(x_i, y_i) is the pixel value, it requires interpolation for subpixel
    accuracy.  
- Utilities
  - [map_coordinates from scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.map_coordinates.html#scipy.ndimage.map_coordinates)
  - [use numba to accelerate by gpu](https://stackoverflow.com/questions/62679777/how-to-accelerate-scipy-map-coordinates-for-multiple-interpolations)
  - [maybe this one works too](https://scikit-image.org/docs/dev/api/skimage.transform.html#skimage.transform.warp)



## Method: Fit ellipse profile to ag behenate image (from maxpool)

It requires eyeballing to recoginze patterns as prior knowledge (prior model).  

It might not work as several profiles are involved, sine wave, gaussian and some
profiles that are not able to assess by eyeballing.  

### Resources about determining an ellipse with three given points

- [link](https://stackoverflow.com/questions/28281742/fitting-a-circle-to-a-binary-image)
- [link](https://math.stackexchange.com/questions/339126/how-to-draw-an-ellipse-if-a-center-and-3-arbitrary-points-on-it-are-given)
- [link](http://benpaulthurstonblog.blogspot.com/2015/11/elliptical-pizza-theorem.html)


### Procedures for finding the beam center

- [circle model] Click three points to determine a circle that roughly fits signals from an
  input image.  
  - The parameters of the circle will be used for downstream fitting an ellipse.  
- [ellipse model] Fitting a more accurate ellipse with a new geometry and location.  


### Profile fitting candidate models

- [2D sine wave](https://stackoverflow.com/questions/27633985/plotting-wave-equation)
- [ring profile](https://www.mathworks.com/matlabcentral/answers/305666-gaussian-ring-in-2d)


## Misc

### Generate the max pooled image.

Use `psocake`.  
