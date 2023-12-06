import imageio


def create_gif(image_arrays, gif_filename, duration=0.1):
    """
    Create a GIF from a list of NumPy RGB arrays.

    Parameters:
    - image_arrays: List of NumPy arrays, each representing an RGB image.
    - gif_filename: Filename for the output GIF.
    - duration: Duration of each frame in the GIF, in seconds.
    """
    with imageio.get_writer(gif_filename, mode='I', duration=duration) as writer:
        for img in image_arrays:
            writer.append_data(img)
