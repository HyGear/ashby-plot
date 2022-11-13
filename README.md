# ashby-plot
A simple script that utilizes numpy and matplotlib to create "Ashby" plots similar to those created by Ansys Granta (see sample plot). The script works by reading data points for the material property from a directory of csv files. After the data is read in, the convex hull of the data points is found and these points are then used to create a closed spline through the convex hull points. Finally, each closed spline is filled with a randomly generated color.

At the moment the script is very crude and is hard coded to plot Density on the x-axis and Young's Modulus on the y-axis as a log-log plot. Future plans are to allow the selection of material property for each axis and filtering of material type along with a simple GUI.

Sample data has been included for several thermoplastic materials so that function of the script can be verified. This data was compiled from Matweb.com.
