from shiny import App, Inputs, Outputs, Session, render, ui, reactive
import hydrogen_wavefunctions as hwf
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import shinyswatch

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
        
        document.addEventListener('DOMContentLoaded', function() {
            sendElementAspectRatio('sidebarPlot');
        });
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
        """),
        ui.tags.script(src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS_HTML"),
    ),

    ui.panel_title(
        ('Hydrogen Wavefunction'),
        ),

    ui.markdown(
            """
            This app graphs the solutions obtained from the time-independent 
            Shrodinger equation for the hydrogen atom by taking the quantum numbers ```n```, 
            ```l```, and ```m```. The hydrogen atom is a 2-body problem, but can be
            simplified with the reduced mass assumption: 

            $$ 
            \mu = \\frac{m_p m_e}{m_p + m_e}
            $$  
            """
        ),

    ui.card(

        ui.layout_sidebar(
            ui.sidebar(   
                ui.input_numeric("n","Principal quantum number, n", value=1),
                ui.input_numeric("l","Azimuthal quantum number, l", value=0),
                ui.input_numeric("m","Magnetic quantum number, m", value=0),
                ui.input_numeric("a0",("Scaling factor, a", ui.tags.sub(0)), value=0.7)
            ),
            {"style": "background-color: #000000"},
            {"id": "sidebarPlot"},
            ui.output_plot("plot1"),
        ),
    ),

    ui.output_text('aspect_ratio'),
    ui.output_text('window_width'),
    ui.output_text('window_height')

)

def server(input, output, session):

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

        a0_scale_factor = input.a0()
        n = input.n()
        l = input.l()
        m = input.m()

        if "sidebarPlot_aspectRatio" in input: 
            x_lower = -500
            x_upper = 500
            x_npoints = x_upper - x_lower
            x = np.linspace(x_lower,x_upper,x_npoints)

            buffer = 1.1

            y_lower = round(x_lower/(input.sidebarPlot_aspectRatio()*buffer))
            y_upper = round(x_upper/(input.sidebarPlot_aspectRatio()*buffer))
            y_npoints = y_upper - y_lower
            y = np.linspace(y_lower, y_upper, y_npoints)
            x,y = np.meshgrid(x,y)

            width_px = input.sidebarPlot_windowWidth()
            height_px = width_px / input.sidebarPlot_aspectRatio() 
            dpi = 100

            fig, ax = plt.subplots()
            fig.set_facecolor('#000000')
            plt.figure(figsize = (width_px / dpi, height_px / dpi), dpi = dpi)
            ax.set_position([0, 0, 1, 1])
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            psi = hwf.wave_function(a0_scale_factor, n, l, m, x, y)
            prob_density = hwf.probability_density(psi)
            ax.imshow(np.sqrt(prob_density), cmap = mpl.colormaps['magma'])
            fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
            
            return fig

        #else:
            #x = np.linspace(-500,500,1000)
            #y = np.linspace(-500,500,1000)
            #x,y = np.meshgrid(x,y)
            #prob_density = hwf.probability_density(psi)
            #ax.imshow(np.sqrt(prob_density), cmap = mpl.colormaps['magma'])
            #plt.gca().set_aspect(input.sidebarPlot_aspectRatio())
            #return fig

        # Compute and visualize the wavefunction probability density
        #psi = hwf.wave_function(a0_scale_factor, n, l, m, x, y)
        #prob_density = hwf.probability_density(psi)
        #ax.imshow(np.sqrt(prob_density), cmap = mpl.colormaps['magma'])
        #ax.text(500,-100, f'(n, l, m) = ({n}, {l}, {m})', color='#dfdfdf', fontsize='large', ha='center',
        #        va='top') 
        #ax.xaxis.set_visible(False)
        #ax.yaxis.set_visible(False)
        #fig.tight_layout()
        #fig.savefig('fig.png')
        return fig

app = App(app_ui, server, debug = True)        

