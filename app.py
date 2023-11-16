from shiny import App, Inputs, Outputs, Session, render, ui, reactive
import hydrogen_wavefunctions as hwf
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import shinyswatch

app_ui = ui.page_fluid(
    shinyswatch.theme.darkly(),
    ui.card(
        ui.layout_sidebar(
            ui.sidebar(   
                ui.input_numeric("n","Principal quantum number, n", value=1),
                ui.input_numeric("l","Azimuthal quantum number, l", value=0),
                ui.input_numeric("m","Magnetic quantum number, m", value=0),
                ui.input_numeric("a0","Scaling factor, a0", value=0.7)
            ),
            {"style": "background-color: #000000"},
            ui.output_plot("plot1"),
        ),
    ),
)

def server(input, output, session):
    
    @output
    @render.plot()
    def plot1():

        a0_scale_factor = input.a0()
        n = input.n()
        l = input.l()
        m = input.m()

        fig, ax = plt.subplots()
        fig.set_facecolor('#000000')

        # Compute and visualize the wavefunction probability density
        psi = hwf.wave_function(a0_scale_factor, n, l, m)
        prob_density = hwf.probability_density(psi)
        ax.imshow(np.sqrt(prob_density), cmap = mpl.colormaps['magma'])
        ax.text(500,0, r'(n, l, m) = $({0}, {1}, {2})$'.format(n, l, m), color='#dfdfdf', fontsize='large') 
        #ax.xaxis.set_visible(False)
        #ax.yaxis.set_visible(False)
        fig.tight_layout()
        return fig

app = App(app_ui, server, debug = True)        

