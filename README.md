# shiny_hydrogen_wf

## Objectives and Overview

This is an app for graphing the probability density wavefunctions for a hydrogen 
atom. First and foremost this was an excuse to play around with the relatively new
[Shiny for Python](https://shiny.posit.co/py/docs/overview.html).   

## Usage

After installing libraries, ```app.py``` runs a Shiny application through the default browser at ```http://localhost```. The app uses an accordion ui element to hide and reveal sections of markdown and plots. A javascript ui element runs on initation to get window size, and updates when window size changes. This is then fed to probability density plots to display the correct aspect ratio.

The app graphs the probability density plot on the left, and the probability specific to the radial componenent on the right. User accepted inputs are the three quantum numbers ```n```, ```l```, and ```m```, as well as a *Bohr* radius scaling factor to help visualize these functions.

![ui](ui.png)

## Sources
- University of Washington, Seattle, Phys 227 lecture notes: https://faculty.washington.edu/seattle/physics227/reading/reading-26-27.pdf, for angular and radial component solutions (pages 337 and 347, respectively).
-  https://github.com/ssebastianmag/hydrogen-wavefunctions/, for how to use ```scipy.special``` to write the associated *Legendre* and *Laguerre* polynomials.

## To-Do
- Add error handling for quantum numbers (or limit user inputs)
- Add dark mode toggle


