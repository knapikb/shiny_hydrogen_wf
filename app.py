from shiny import App, Inputs, Outputs, Session, render, ui, reactive
import hydrogen_wavefunctions as hwf
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import shinyswatch

app_ui = ui.page_fluid(
    shinyswatch.theme.darkly(),
    ui.tags.style("body {font-family: Times}"),
    ui.panel_title(
        ('Hydrogen Wavefunctions'),
        ),
    ui.h3(
        (' e',ui.tags.sup('-'),' Probability Distribution'),
        style = f"font-size:1;"),
    ui.card(
        ui.layout_sidebar(
            ui.sidebar(   
                ui.input_numeric("n","Principal quantum number, n", value=1),
                ui.input_numeric("l","Azimuthal quantum number, l", value=0),
                ui.input_numeric("m","Magnetic quantum number, m", value=0),
                ui.input_numeric("a0",("Scaling factor, a", ui.tags.sub(0)), value=0.7)
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
        plt.rcParams["font.family"] = "Times"
        prob_density = hwf.probability_density(psi)
        ax.imshow(np.sqrt(prob_density), cmap = mpl.colormaps['magma'])
        ax.text(480,0, f'(n, l, m) = ({n}, {l}, {m})', color='#dfdfdf', fontsize='large', ha='center',
                va='top') 
        #ax.xaxis.set_visible(False)
        #ax.yaxis.set_visible(False)
        fig.tight_layout()
        return fig

app = App(app_ui, server, debug = True)        

