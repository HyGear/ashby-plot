# ashby-plot
A simple script that generates "Ashby" plots similar to those explained in the book "Materials Selection in Mechanical Design" by Michael F. Ashby. The script works by reading material information from a CSV file into the local database. After the data is read in, the convex hull of the data points is found and these points are then used to create a closed spline through the convex hull points. Finally, each closed spline is filled with color based on the currently selected color scheme.

The latest update of the script has a usable GUI and presets of all the basic Ashby plots. It also includes enough material data to check the basic function of the application.

![Ashby pot](https://raw.githubusercontent.com/HyGear/ashby-plot/refs/heads/main/screenshots/ashby-screenshot.png)
