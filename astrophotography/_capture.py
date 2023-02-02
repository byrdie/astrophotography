import pathlib
import matplotlib.pyplot as plt
import astropy.units as u
import astropy.time
import astropy.coordinates
import astropy.io.fits
import cv2

__all__ = [
    'capture',
]


def capture(
        camera_id: int,
        exposure_value: int,
        directory: pathlib.Path,
        location: astropy.coordinates.EarthLocation,
        target: str,
        focal_length: u.Quantity,
        pixel_size: u.Quantity,
):

    directory.mkdir(exist_ok=True)

    camera = cv2.VideoCapture(camera_id)
    camera.set(cv2.CAP_PROP_EXPOSURE, exposure_value)

    ret, frame = camera.read()

    fig = plt.figure()
    img = plt.imshow(frame)

    num_images = 0
    while True:

        try:
            time = astropy.time.Time.now()
            header = astropy.io.fits.Header()
            header['TIME'] = str(time.fits)
            header['LATITUDE'] = location.lat.value
            header['LONGITUDE'] = location.lon.value
            header['ELEVATION'] = location.height.value
            header['TARGET'] = target
            header['FOCAL_LENGTH'] = focal_length.to_value(u.mm)
            header['PIXEL_SIZE'] = pixel_size.to_value(u.um)

            _, data = camera.read()

            hdu = astropy.io.fits.PrimaryHDU(data=data, header=header)

            filename = directory / f"{time.strftime('%Y-%m-%dT%H-%M-%S-%f')}.fits"
            astropy.io.fits.HDUList([hdu]).writeto(filename)

            print(f"Saved {filename}")

            num_images += 1

            img.set_data(data)
            plt.draw()
            plt.pause(1e-6)

        except KeyboardInterrupt:
            print(f"Exiting, captured {num_images}")
            break

    plt.close(fig)

