import imageIO as io
import stats as st
import contrast as ct
import filters as filt
from image import ImageModel

import math
import matplotlib
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import Counter
from datetime import datetime 
from tkinter import ttk
from PIL import Image

class main_app:
    def __init__(self, window):
        self.window = window
        self.window.title('Image Processing')
        self.window.geometry(f'{self.window.winfo_screenwidth()-10}x{self.window.winfo_screenheight()-95}+1+0')
        self.window.resizable(False,False)
        self.init_interface()
        self.orig_image = ImageModel()
        self.new_image = ImageModel()

    def init_interface(self):
        root_menu = tk.Menu(self.window)
        self.window.config(menu=root_menu)

        image_menu = tk.Menu(root_menu, tearoff=0)

        image_menu.add_command(label="Histogram")
        image_menu.add_command(label="Cumulitive Histogram")
        image_menu.add_separator()
        image_menu.add_command(label="Dark Dilatation")
        image_menu.add_command(label="Light Dilatation")
        image_menu.add_command(label="Middle Dilatation")
        image_menu.add_command(label="Inverse")
        root_menu.add_cascade(label="Original Image Histogram", menu=image_menu)
        root_menu.add_command(label="Contrast Modification")

        # ***********    Origin Image Frame ************

        orig_image_frame = tk.Frame(self.window,width=self.window.winfo_screenwidth() * 0.25)
        orig_image_frame.pack_propagate(0)
        orig_image_frame.pack(anchor=tk.W, side=tk.LEFT, fill=tk.Y, expand=tk.YES)
            
            # ***********    Open Image ************

        file_frame = tk.Frame(orig_image_frame, height=100, width=100, pady=5)
        tk.Label(file_frame,fg="red", text="Start by choosing your image*").grid(row=0, column=0, columnspan=2, padx=2)
        tk.Label(file_frame, text="Image Path:").grid(row=1, column=0, padx=2)
        self.file_name = tk.Entry(file_frame, width=30)
        self.file_name.grid(row=1, column=1, padx=10)
        tk.Button(file_frame, text="Open", padx=10, pady=5, command=self.open_callback).grid(row=1, column=2,padx=10)
        file_frame.pack(anchor=tk.NW,padx=10)

        ttk.Separator(orig_image_frame, orient='horizontal').pack(fill='x', pady=5)

            # ***********    Image Place      ************

        image_frame = tk.Frame(orig_image_frame, width=self.window.winfo_screenwidth() * 0.25, height=300, pady=5)
        tk.Label(image_frame, text="Original Image:").pack(padx=10)
        self.orig_fig = Figure(figsize=(6, 5), dpi=100)
        self.orig_ax = self.orig_fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(self.orig_fig, image_frame)
        plot_widget = canvas.get_tk_widget()
        plot_widget.config(width=self.window.winfo_screenwidth() * 0.25, height=300)
        plot_widget.pack(expand=tk.YES, anchor=tk.CENTER, pady=5, padx=5)
        image_frame.pack_propagate(0)
        image_frame.pack(anchor=tk.NW,padx=10)

        ttk.Separator(orig_image_frame, orient='horizontal').pack(fill='x', pady=5)

            # ***********    Image Histogram ************

        histogram_frame = tk.Frame(orig_image_frame, width=100, height=300, pady=5)
        tk.Label(histogram_frame, text="Generate Histogram and cumulitive Histogram:").grid(row=0,column=0)
        self.generate_hists_button = tk.Button(histogram_frame, text="Generate", padx=10, pady=5, command=self.generate_hists_callback,state=tk.DISABLED)
        self.generate_hists_button.grid(row=0, column=1,columnspan=3,padx=10)
        histogram_frame.pack_propagate(0)
        histogram_frame.pack()

        ttk.Separator(orig_image_frame, orient='horizontal').pack(fill='x', pady=5)

            # ***********    Image Properties ************

        properties_frame = tk.Frame(orig_image_frame, height=100, width=100, pady=5)

        tk.Label(properties_frame,fg='red', text="Image properties:").grid(row=0, column=0, columnspan=3, padx=2,pady=5)

        tk.Label(properties_frame, text="Width:").grid(row=1, column=0, padx=10,pady=(10,5),sticky="w")
        self.width_text = tk.Label(properties_frame, text="0", width=30, relief=tk.SUNKEN)
        self.width_text.grid(row=1, column=2,sticky='w')

        tk.Label(properties_frame, text="Length:").grid(row=2, column=0, padx=10,pady=5,sticky="w")
        self.height_text = tk.Label(properties_frame, text="0", width=30, relief=tk.SUNKEN)
        self.height_text.grid(row=2, column=2,sticky='w')

        tk.Label(properties_frame, text="Number of pixels:").grid(row=3, column=0, padx=10,pady=5, sticky="w")
        self.pixel_text = tk.Label(properties_frame, text="0", width=30, relief=tk.SUNKEN)
        self.pixel_text.grid(row=3, column=2,sticky='w')

        properties_frame.pack(anchor=tk.NW,padx=10)

        ttk.Separator(orig_image_frame, orient='horizontal').pack(fill='x', pady=5)

            # ***********    Image Metrics ************  

        stat_frame = tk.Frame(orig_image_frame, height=100, width=100)

        tk.Label(stat_frame,fg='red', text="Image stats:").grid(row=0, column=0, columnspan=3, padx=2,pady=5)

        tk.Label(stat_frame, text="Mean:").grid(row=1, column=0, padx=10,pady=5,sticky='w')
        self.mean_text = tk.Label(stat_frame, text="0", width=28, relief=tk.SUNKEN)
        self.mean_text.grid(row=1, column=2,sticky='w')

        tk.Label(stat_frame, text="Variance:").grid(row=2, column=0, padx=10,pady=5,sticky='w')
        self.variance_text = tk.Label(stat_frame, text="0", width=28, relief=tk.SUNKEN)
        self.variance_text.grid(row=2, column=2,sticky='w')

        tk.Label(stat_frame, text="Standard deviation:").grid(row=3, column=0, padx=10,pady=5,sticky='w')
        self.deviation_text = tk.Label(stat_frame, text="0", width=28, relief=tk.SUNKEN)
        self.deviation_text.grid(row=3, column=2,sticky='w')

        tk.Label(stat_frame, text="Entropy:").grid(row=4, column=0, padx=10,pady=5,sticky='w')
        self.entropy_text = tk.Label(stat_frame, text="0", width=28, relief=tk.SUNKEN)
        self.entropy_text.grid(row=4, column=2,sticky='w')
        
        stat_frame.pack(anchor=tk.NW,padx=10)

        # ***********    New Image Frame ************  

        new_image_frame = tk.Frame(self.window,width=self.window.winfo_screenwidth() * 0.45)
        new_image_frame.pack_propagate(0)
        new_image_frame.pack(anchor=tk.W, fill=tk.Y,side=tk.LEFT, expand=tk.YES)

        tk.Label(new_image_frame, text="New Edited Image:",fg='red').pack(padx=10)
        self.new_fig = Figure(figsize=(20, 20), dpi=100)
        self.new_ax = self.new_fig.add_subplot(111)
        canvas2 = FigureCanvasTkAgg(self.new_fig, new_image_frame)
        plot_widget2 = canvas2.get_tk_widget()
        plot_widget2.config(width=self.window.winfo_screenwidth() * 0.45, height=600)
        plot_widget2.pack(expand=tk.YES, anchor=tk.CENTER, padx=5)

        console_frame = tk.Frame(new_image_frame, height=100, width=self.window.winfo_screenwidth() * 0.45,pady=10)
        self.console = tk.Text(console_frame, height=10, width=100, fg="red",state=tk.DISABLED,bg="lightgrey")
        self.console.pack()
        console_frame.pack(anchor=tk.S, side=tk.BOTTOM,padx=5)


        # ***********    New Image Data Frame ************ 

        new_image_data_frame = tk.Frame(self.window,width=self.window.winfo_screenwidth() * 0.25)
        new_image_data_frame.pack_propagate(0)
        new_image_data_frame.pack(anchor=tk.W, fill=tk.Y,side=tk.LEFT, expand=tk.YES)

            # ***********    Saving New Edited Image ************ 

        file_frame = tk.Frame(new_image_data_frame, height=100, width=100, pady=5)
        tk.Label(file_frame,fg="red", text="Save your new image*").grid(row=0, column=0, columnspan=2)
        tk.Label(file_frame, text="Save your file with (.pgm) extension").grid(row=1, column=0)
        self.save_button = tk.Button(file_frame, text="Save Image as", padx=10, pady=5, command=self.save_callback,state=tk.DISABLED)
        self.save_button.grid(row=1, column=1,columnspan=2,padx=10)
        file_frame.pack(anchor=tk.NW,padx=10)

        ttk.Separator(new_image_data_frame, orient='horizontal').pack(fill='x', pady=5)

            # ***********    Different Operations ************ 

        operations_frame = tk.Frame(new_image_data_frame, height=100, width=100, pady=5)
        tk.Label(operations_frame, text="Histogram equalization").grid(row=0, column=0)
        self.histogram_equalization = tk.Button(operations_frame, text="Equalize", padx=10, pady=5, command=self.equalize_callback,state=tk.DISABLED)
        self.histogram_equalization.grid(row=0, column=1,padx=10)
        tk.Label(operations_frame, text="Define A(x,y) and B(z,w) for contrast function (x <= z)").grid(row=1, column=0,columnspan=10,padx=5,pady=5,sticky='w')

        contrast_function_frame = tk.Frame(new_image_data_frame, height=100, width=100, pady=5)
        
        tk.Label(contrast_function_frame, text="Point A (x,y):").grid(row=2, column=0,pady=5,padx=5,sticky='w')
        self.A_x = tk.Entry(contrast_function_frame, width=5, relief=tk.SUNKEN)
        self.A_x .grid(row=2, column=1,sticky='w',padx=5)
        self.A_y = tk.Entry(contrast_function_frame,width=5, relief=tk.SUNKEN)
        self.A_y .grid(row=2, column=2,sticky='w',padx=5)

        tk.Label(contrast_function_frame, text="Point B (z,w):").grid(row=3, column=0,pady=5,padx=5,sticky='w')
        self.B_x = tk.Entry(contrast_function_frame, width=5, relief=tk.SUNKEN)
        self.B_x.grid(row=3, column=1,sticky='w',padx=5)
        self.B_y = tk.Entry(contrast_function_frame, width=5, relief=tk.SUNKEN)
        self.B_y.grid(row=3, column=2,sticky='w',padx=5)

        self.contrast_button = tk.Button(contrast_function_frame, text="Contrast Function", padx=10, pady=5, command=self.contrast_function_callback,state=tk.DISABLED)
        self.contrast_button.grid(row=2, column=3,rowspan=2,padx=10)

        operations_frame.pack(anchor=tk.NW,padx=10)
        contrast_function_frame.pack(anchor=tk.NW,padx=10)
    
        ttk.Separator(new_image_data_frame, orient='horizontal').pack(fill='x', pady=5)

            # ***********   Other Operations    ************

                
        buttons_frame = tk.Frame(new_image_data_frame, height=100, width=100, pady=5)

        tk.Label(buttons_frame, text="Other operations").grid(row=0, column=0,columnspan=3)
        self.add_noise = tk.Button(buttons_frame, text="Add noise",width=10, padx=10, pady=5, command=self.add_noise,state=tk.DISABLED)
        self.add_noise.grid(row=1, column=0,padx=10)

        tk.Label(buttons_frame, text="Choose filter size:").grid(row=1, column=1,pady=5,padx=5,sticky='w')
        self.filter_size = tk.Entry(buttons_frame, width=5,state=tk.DISABLED, relief=tk.SUNKEN)
        self.filter_size .grid(row=1, column=2,sticky='w',padx=5)
        
        self.average_filter = tk.Button(buttons_frame, text="Average filter", padx=10, pady=5, command=self.average_filter,state=tk.DISABLED)
        self.average_filter.grid(row=2, column=0,padx=10)
        self.median_filter = tk.Button(buttons_frame, text="Median filter", padx=10, pady=5, command=self.median_filter,state=tk.DISABLED)
        self.median_filter.grid(row=2, column=1,padx=10)
        self.gauss_filter = tk.Button(buttons_frame, text="Gaussian filter", padx=10, pady=5, command=self.gauss_filter,state=tk.DISABLED)
        self.gauss_filter.grid(row=2, column=2,padx=10,pady=(0,5))
        self.high_filter = tk.Button(buttons_frame, text="High filter",width=10, padx=10, pady=5, command=self.high_filter,state=tk.DISABLED)
        self.high_filter.grid(row=3, column=0,padx=10)
        self.laplace_filter = tk.Button(buttons_frame, text="Laplace filter", padx=10, pady=5, command=self.laplace_filter,state=tk.DISABLED)
        self.laplace_filter.grid(row=3, column=1,padx=10)
        
        buttons_frame.pack(anchor=tk.NW,padx=10)
        buttons_frame.pack(anchor=tk.NW,padx=10)
    
        ttk.Separator(new_image_data_frame, orient='horizontal').pack(fill='x', pady=5)
            # ***********    Compare Histograms ************ 

        histogram_comparison_frame = tk.Frame(new_image_data_frame, width=100, height=300, pady=5)
        tk.Label(histogram_comparison_frame, text="Compare Histograms (Original vs New):").grid(row=0,column=0,padx=5,sticky='w')
        self.generate_compare_hists_button = tk.Button(histogram_comparison_frame, text="Generate", pady=5, command=self.generate_compare_hists_callback,state=tk.DISABLED)
        self.generate_compare_hists_button.grid(row=0, column=1,columnspan=3,padx=10)
        histogram_comparison_frame.pack_propagate(0)
        histogram_comparison_frame.pack(anchor=tk.NW,padx=10)

        ttk.Separator(new_image_data_frame, orient='horizontal').pack(fill='x', pady=5)

          # ***********    New Image Metrics ************  

        new_stat_frame = tk.Frame(new_image_data_frame, height=100, width=100)

        tk.Label(new_stat_frame,fg='red', text="New Image stats:").grid(row=0, column=0, columnspan=3, padx=2,pady=5)

        tk.Label(new_stat_frame, text="Mean:").grid(row=1, column=0, padx=10,pady=5,sticky='w')
        self.new_mean_text = tk.Label(new_stat_frame, text="0", width=28, relief=tk.SUNKEN)
        self.new_mean_text.grid(row=1, column=2,sticky='w')

        tk.Label(new_stat_frame, text="Variance:").grid(row=2, column=0, padx=10,pady=5,sticky='w')
        self.new_variance_text = tk.Label(new_stat_frame, text="0", width=28, relief=tk.SUNKEN)
        self.new_variance_text.grid(row=2, column=2,sticky='w')

        tk.Label(new_stat_frame, text="Standard deviation:").grid(row=3, column=0, padx=10,pady=5,sticky='w')
        self.new_deviation_text = tk.Label(new_stat_frame, text="0", width=28, relief=tk.SUNKEN)
        self.new_deviation_text.grid(row=3, column=2,sticky='w')

        tk.Label(new_stat_frame, text="Entropy:").grid(row=4, column=0, padx=10,pady=5,sticky='w')
        self.new_entropy_text = tk.Label(new_stat_frame, text="0", width=28, relief=tk.SUNKEN)
        self.new_entropy_text.grid(row=4, column=2,sticky='w')
        
        tk.Label(new_stat_frame, text="SNR:").grid(row=5, column=0, padx=10,pady=5,sticky='w')
        self.new_snr_text = tk.Label(new_stat_frame, text="0", width=28, relief=tk.SUNKEN)
        self.new_snr_text.grid(row=5, column=2,sticky='w')
        new_stat_frame.pack(anchor=tk.NW,padx=10)
            
    
    def open_callback(self):
        try:
            file = tk.filedialog.askopenfilename(        
                title="Open PGM file", 
                filetypes=(("PGM Files", "*.pgm"),))
            io.read_pgm(file,self.orig_image)
            io.read_pgm(file, self.new_image)
            self.update_orig_stats()
            self.update_new_image()
            self.write_console(f'New image opened.\n({file})')
            self.file_name.delete(0,tk.END)
            self.file_name.insert(0,file)
        except Exception:
            self.write_console('readError: error with ' + self.entry_text.get() + ': has wrong type or size.\n')
        except FileNotFoundError:
            self.write_console("File not found, try again.")

    def save_callback(self):
        try:
            file = tk.filedialog.asksaveasfilename(        
                title="Save PGM file", 
                filetypes=(("PGM Files", "*.pgm"),))
            io.write_pgm(self.new_image.get_data(), file)
            self.update_orig_stats()
            self.write_console(f'Image saved !\n(path: {file})')
        except Exception:
            self.write_console('readError: Something went wrong !!')
    
    def update_orig_stats(self):
        self.width_text.config(text=str(self.orig_image.width))
        self.height_text.config(text=str(self.orig_image.height))
        self.pixel_text.config(text=str(self.orig_image.get_num_pixels()))
        mean,var = st.stat_image(self.orig_image.data)
        self.mean_text.config(text=str(mean))
        self.variance_text.config(text=str(var))
        self.deviation_text.config(text=str(math.sqrt(var)))
        self.entropy_text.config(text=str(st.entropy(self.orig_image.get_data())))
        self.generate_hists_button.config(state=tk.NORMAL)
        self.display_orig_image()

    def update_new_image(self):
        self.save_button.config(state=tk.NORMAL)
        # contrast
        self.histogram_equalization.config(state=tk.NORMAL)
        self.contrast_button.config(state=tk.NORMAL)
        # other operations buttons
        self.add_noise.config(state=tk.NORMAL)
        self.average_filter.config(state=tk.NORMAL)
        self.laplace_filter.config(state=tk.NORMAL)
        self.median_filter.config(state=tk.NORMAL)
        self.high_filter.config(state=tk.NORMAL)
        self.filter_size.config(state=tk.NORMAL)
        # hist button
        self.generate_compare_hists_button.config(state=tk.NORMAL)
        # stats 
        mean,var = st.stat_image(self.new_image.data)
        self.new_mean_text.config(text=str(mean))
        self.new_variance_text.config(text=str(var))
        self.new_deviation_text.config(text=str(math.sqrt(var)))
        self.new_entropy_text.config(text=str(st.entropy(self.new_image.get_data())))
        self.display_new_image()
        self.new_image.is_noise = False

    def display_orig_image(self):
        self.orig_ax.clear()
        self.orig_ax.imshow(Image.fromarray(self.orig_image.data))
        self.orig_fig.canvas.draw()

    def display_new_image(self):
        self.new_ax.clear()
        self.new_ax.imshow(Image.fromarray(self.new_image.data))
        self.new_fig.canvas.draw()

    def generate_hists_callback(self):
        st.generate_histograms(self.orig_image.get_data())

    def equalize_callback(self):
        width,height,gray_level,final_image = ct.Histogram_egalisation(self.orig_image.get_data())
        self.new_image.set_attributes(width, height, gray_level, final_image)
        self.write_console("Image histogram equalized !")
        self.update_new_image()

    def contrast_function_callback(self):
        a_x = self.A_x.get()
        a_y = self.A_y.get()
        b_x = self.B_x.get()
        b_y = self.B_y.get()
        a_point = ct.Point(int(a_x), int(a_y),self.orig_image.gray_level,self.write_console)
        b_point = ct.Point(int(b_x), int(b_y), self.orig_image.gray_level,self.write_console)
        if(ct.check_points(a_point,b_point) == False):
            self.write_console("invalid points, A should be inferior to B")
        else:
            width,height,gray_level,final_image = ct.contrast_modifier(a_point, b_point, self.orig_image.get_data())
            self.new_image.set_attributes(width, height, gray_level, final_image)
            self.write_console("Contrast function applied !")
            self.update_new_image()
    
    def generate_compare_hists_callback(self):
        self.write_console("Generating Figures ...")
        st.generate_compare_histograms(self.orig_image.get_data(),self.new_image.get_data())
        self.write_console("Figures generated ...")

    def add_noise(self):
        width,height,gray_level,final_image = filt.add_noise(self.orig_image.get_data())
        self.new_image.set_attributes(width, height, gray_level, final_image)
        self.new_image.is_noise = True
        self.write_console("Noise added !")
        self.update_new_image()
    
    def get_image_noise_data(self):
        if(self.new_image.is_noise):
            return self.new_image.get_data()
        else:
            return self.orig_image.get_data()
        
    def average_filter(self):
        size = self.filter_size.get()
        if(size == ""):
            self.write_console("Add filter size !!")
        else:
            data = self.get_image_noise_data()
            width,height,gray_level,final_image = filt.average_filter(data, int(size))
            self.new_image.set_attributes(width, height, gray_level, final_image)
            self.write_console("Average filter applied !")
            self.update_new_image()
            self.new_snr_text.config(text=str(filt.SNR(self.orig_image.get_data(), self.new_image.get_data())))
            
    def median_filter(self):
        size = self.filter_size.get()
        if(size == ""):
            self.write_console("Add filter size !!")
        else:
            data = self.get_image_noise_data()
            width,height,gray_level,final_image = filt.median_filter(data,int(size))
            self.new_image.set_attributes(width, height, gray_level, final_image)
            self.write_console("Median filter applied !")
            self.update_new_image()
            self.new_snr_text.config(text=str(filt.SNR(self.orig_image.get_data(), self.new_image.get_data())))

    def gauss_filter(self):
        size = self.filter_size.get()
        if(size == ""):
            self.write_console("Add filter size !!")
        else:
            data = self.get_image_noise_data()
            width,height,gray_level,final_image = filt.gauss_filter(data, int(size))
            self.new_image.set_attributes(width, height, gray_level, final_image)
            self.write_console("Gauss filter applied !")
            self.update_new_image()
            self.new_snr_text.config(text=str(filt.SNR(self.orig_image.get_data(), self.new_image.get_data())))

    
    def high_filter(self):
        width,height,gray_level,final_image = filt.high_filter(self.orig_image.get_data())
        self.new_image.set_attributes(width, height, gray_level, final_image)
        self.write_console("High filter applied !")
        self.update_new_image()
        self.new_snr_text.config(text=str(filt.SNR(self.orig_image.get_data(), self.new_image.get_data())))

    
    def laplace_filter(self):
        width,height,gray_level,final_image = filt.laplace_filter(self.orig_image.get_data())
        self.new_image.set_attributes(width, height, gray_level, final_image)
        self.write_console("Laplace filter applied !")
        self.update_new_image()
        self.new_snr_text.config(text=str(filt.SNR(self.orig_image.get_data(), self.new_image.get_data())))

    def write_console(self, text):
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END,f'{datetime.today().strftime("%Y-%m-%d %H:%M:%S")} : {text}\n' )
        self.console.config(state=tk.DISABLED)

main_screen = tk.Tk()
main_app(main_screen)
main_screen.mainloop()