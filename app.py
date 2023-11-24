from shiny import App, Inputs, Outputs, Session, render, ui, reactive
import hydrogen_wavefunctions as hwf
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import shinyswatch
import math

"""
TO DO: 
- Need error handling for incorrect selection of quantum numbers
- Light vs. dark mode toggle
"""

app_ui = ui.page_fluid(
    shinyswatch.theme.darkly(),
    
    ui.tags.script("""
        function sendElementAspectRatio(elementId) {
            var element = document.getElementById(elementId);
            if (element) {
                var rect = element.getBoundingClientRect();
                var windowWidth = rect.width;
                var windowHeight = rect.height;
                var aspectRatio = rect.width / rect.height;
                Shiny.setInputValue(elementId + '_aspectRatio', aspectRatio);
                Shiny.setInputValue(elementId + '_windowWidth', windowWidth);
                Shiny.setInputValue(elementId + '_windowHeight', windowHeight);
            }
        }

        window.onresize = function() {
            sendElementAspectRatio('sidebarPlot');
        };
    """),
    
    ui.tags.head(
        ui.tags.style("""
        body {
            font-family: 'Times New Roman', Times, serif;
        }
        ),
        .sidebar-panel {
            padding: 0 !important;
        }
        .accordion-title {
                font-size: 24px !important;
            }
        }
        """),
        ui.tags.script(src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS_HTML"),
    ),

    ui.panel_title(
        ('Hydrogen Wavefunctions'),
        ),

        ui.markdown(
            """
            <br>

            This app graphs the solutions obtained from the time-independent 
            Schrödinger equation of a single particle of mass ```m``` in a field ```V```. 

            $$
                (-\\frac{\\hbar^2}{2 m} \\nabla^2 + V ) \\psi = E \\psi
            $$  
            
            """
        ),

    ui.accordion_panel(f"Methods Overview",{"accordion-title":"font-size:10px"},

    ui.markdown(
            """
            Expanding the Laplacian operator in spherical coordinates, the Schrödinger equation becomes:

            $$
                \\frac{-\\hbar^2}{2m} \\left[\\frac{1}{r^2}\\frac{\\partial}{\\partial r}
                \\left(r^2 \\frac{\\partial}{\\partial r} \\right) + \\frac{1}{r^2 \\sin \\theta}
                \\frac{\\partial}{\\partial \\theta} \\left(\\sin \\theta \\frac{\\partial}{\\partial \\theta} 
                \\right) + \\frac{1}{r^2 \\sin^2 \\theta} \\frac{\\partial^2}{\\partial \\phi^2}
                \\right] \\psi + V(r) \\psi = E \\psi  
            $$ 

            The hydrogen atom is a 2-body problem, but can be greatly
            simplified with the reduced mass assumption:

            $$ 
            m_p \\gg m_e, \\mu = \\frac{m_p m_e}{m_p + m_e} \\sim m_e
            $$

            The analytical solutions to the Schrödinger equation, defined above in 
            spherical coordinates for a singular particle approximating a hydrogen atom,
            is obtained using a separation of variables into radial and angular components. 

            $$
                \\psi(r, \\theta, \\phi) = R(r) Y(\\theta, \\phi)
            $$

            $$
            \\left [ \\frac{1}{R(r)} \\frac{\\partial}{\\partial r} \\left(r^2 \\frac{\\partial}{\\partial r} \\right)
            R(r) - \\frac{2mr^2}{\\hbar^2} \\left[V(r) - E \\right] \\right] + 
            \\left[\\frac{1}{Y(\\theta, \\phi) \\sin\\theta} \\frac{\\partial}{\\partial \\theta}
            \\left(\\sin\\theta \\frac{\\partial}{\\partial \\theta} \\right) Y(\\theta, \\phi) +
            \\frac{1}{Y(\\theta, \\phi) \\sin^2\\theta} \\frac{\\partial^2}{\\partial \\phi^2} Y(\\theta,\\phi)
            \\right] = 0
            $$

            A breakdown of the techniques and derivations used to solve the radial and angular components require 
            quite a bit of heavy lifting. As such, the reader is referred to materials far better suited to covering
            this task: https://faculty.washington.edu/seattle/physics227/reading/reading-26-27.pdf

            """
        ),),
    
    ui.accordion_panel(f"Plots",{"accordion-title":"font-size:10px"},

    ui.markdown(
            """
            Accepts user inputs for quantum numbers ```n```, 
            ```l```, and ```m```. 

            """
        ),
        
    ui.card(
        ui.row(
            ui.column(3, ui.input_numeric("n",ui.markdown("""Principal quantum number, ```n```"""), value=1),
            ),
            ui.column(3, ui.input_numeric("l",ui.markdown("""Azimuthal quantum number, ```l```"""), value=0),
            ),
            ui.column(3, ui.input_numeric("m",ui.markdown("""Magnetic quantum number, ```m```"""), value=0),
            ),
            ui.column(3, ui.input_numeric("a0",("Scaling factor, a", ui.tags.sub(0)), value=10)
            ),

            #ui.input_numeric("n","Principal quantum number, n", value=1),
            #ui.input_numeric("l","Azimuthal quantum number, l", value=0),
            #ui.input_numeric("m","Magnetic quantum number, m", value=0),
            #ui.input_numeric("a0",("Scaling factor, a", ui.tags.sub(0)), value=0.7)
        ),

    ),
    
    ui.row(
        ui.column(6,
                  ui.output_plot("plot1"),
                  {"id": "sidebarPlot"}),
        ui.column(6,
                  ui.output_plot("plot2"),
                  {"style": "background-color: #000000"}),
        ),
    
    ui.row(
            ui.column(6,
                ui.markdown(
                """
                $$
                \\psi(r, \\theta, \\phi) = R(r) Y(\\theta, \\phi)
                $$

                $$
                P_{n, l, m}(r, \\theta, \\phi) = \\langle \\psi | \\psi \\rangle
                $$
                """
                )
            ),

            ui.column(6,ui.markdown(
                """
                $$
                R_{n,l}(r) = \\left[\\frac{\\left(\\frac{2}{na_0}\\right)^3 (n-l-1)!}{2n[(n+l)!]^3} 
                \\right]^{1/2} e^{-\\frac{r}{na_0}} \\left(\\frac{2r}{na_0}\\right)^l L^{2l+1}_{n-l-1} 
                \\left(\\frac{2r}{na_0}\\right)
                $$
                """
                )
                ),),
    ),

    #ui.output_text('aspect_ratio'),
    #ui.output_text('window_width'),
    #ui.output_text('window_height')
)

def server(input, output, session):

    @output
    @render.text
    def radial_markdown_output():
        n = input.n()
        l = input.l()
        markdown = """
                $$
                R_1(r)
                $$
                """
        return markdown

    @output
    @render.text
    def aspect_ratio():
        if "sidebarPlot_aspectRatio" in input:
            return f"Aspect Ratio: {input.sidebarPlot_aspectRatio()}"
        return "Aspect Ratio: Not available"
    
    @output
    @render.text
    def window_width():
        if "sidebarPlot_windowWidth" in input:
            return f"Window width: {input.sidebarPlot_windowWidth()}"
        return "Window width: Not available"
    
    @output
    @render.text
    def window_height():
        if "sidebarPlot_windowHeight" in input:
            return f"Window height: {input.sidebarPlot_windowHeight()}"
        return "Window height: Not available"
    
    @output
    @render.plot()
    def plot1() -> object:

        color_map = 'gist_gray'

        a0_scale_factor = input.a0()
        n = input.n()
        l = input.l()
        m = input.m()

        if "sidebarPlot_aspectRatio" in input: 
            x_lower = -500 # Build grid dependencies for hwf
            x_upper = 500
            x_npoints = x_upper - x_lower
            x = np.linspace(x_lower,x_upper,x_npoints)

            buffer = 1.0

            # Scale grid space based on window aspect ratio
            y_lower = round(x_lower/(input.sidebarPlot_aspectRatio()*buffer))
            y_upper = round(x_upper/(input.sidebarPlot_aspectRatio()*buffer))
            y_npoints = y_upper - y_lower
            y = np.linspace(y_lower, y_upper, y_npoints)
            x,y = np.meshgrid(x,y)

            width_px = input.sidebarPlot_windowWidth()
            height_px = width_px / input.sidebarPlot_aspectRatio() 
            dpi = 100

            # Solve wave functions
            psi = hwf.wave_function(a0_scale_factor, n, l, m, x, y)
            prob_density = hwf.probability_density(psi)

            fig, ax = plt.subplots() # Main plot
            ax.imshow(np.sqrt(prob_density), cmap = mpl.colormaps[color_map])
            
            fig.set_facecolor('#000000') # Plot formatting
            plt.figure(figsize = (width_px / dpi, height_px / dpi), dpi = dpi)
            ax.set_position([0, 0, 1, 1])
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
            
            return fig

        else: # Issues with .js consistency, if not found default to 1:1 aspect ratio 
            x = np.linspace(-500,500,1000) # Build grid dependencies for hwf
            y = np.linspace(-500,500,1000) # 1:1 aspect ratio
            x,y = np.meshgrid(x,y)

            # Solve wave functions
            psi = hwf.wave_function(a0_scale_factor, n, l, m, x, y)
            prob_density = hwf.probability_density(psi)

            fig, ax = plt.subplots() # Main plot
            ax.imshow(np.sqrt(prob_density), cmap = mpl.colormaps[color_map])
            
            fig.set_facecolor('#000000') # Plot formatting
            ax.set_position([0, 0, 1, 1])
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            fig.subplots_adjust(left=0,right=1,top=1,bottom=0)

        return fig
    
    @output
    @render.plot()
    def plot2() -> object:
        from matplotlib.ticker import AutoMinorLocator

        n = input.n()
        l = input.l()
        m = input.m()

        x = np.linspace(-500,500,1000)
        y = np.linspace(-500,500,1000)
        x,y = np.meshgrid(x,y)
        
        r = np.sqrt(x**2 + y**2)
        a0 = 10 # Don't scale Bohr radius for plotting purposes.

        R_nl = hwf.radial_function(a0, n, l, r) # Solve radial equation

        P_r = 4 * math.pi * r**2 * R_nl**2 # Calculate radial probability
        
        fig, ax = plt.subplots() # Main plot
        plt.plot(r/a0,P_r, color = 'white', linewidth = 1)

        plt.gca().set_yticklabels([]) # Plot formatting
        plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
        ax.set_xlim([0, 25])
        plt.xlabel(r'$\frac{r}{a_{0}}$',fontsize='x-large',color='#ffffff')
        plt.ylabel(r'4$\pi$$r^2$ R$_n$$_l^2$',fontsize='medium',color='#ffffff')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')

        for spine in ax.spines.values():
            spine.set_edgecolor('white')

        fig.patch.set_facecolor('#000000') 
        ax.set_facecolor('#000000')
        
        return fig

app = App(app_ui, server, debug = True)     