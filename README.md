 <!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/AdamGoodApp/Flood-sim">
    <img src="https://cdn.dribbble.com/users/46664/screenshots/2855254/dribbble-flood-logo.png?compress=1&resize=800x600" alt="Logo" width="180">
  </a>

  <h3 align="center">Flood Simulation</h3>

  <p align="center">
    Simulate flooding in any area around the world
    <br />
    <br />
    <br />
    <a href="https://youtu.be/OUaLWqVPtmM">View Demo</a>
    ·
    <a href="https://github.com/AdamGoodApp/Flood-sim/labels/bug">Report Bug</a>
    ·
    <a href="https://github.com/AdamGoodApp/Flood-sim/labels/enhancement">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Global mean sea level has risen about 8–9 inches (21–24 centimeters) since 1880, with about a third of that coming in just the last two and a half decades. The rising water level is mostly due to a combination of meltwater from glaciers and ice sheets and thermal expansion of seawater as it warms.

This project simulates world wide flooding based on rising sea levels to provide a visual model for analysis and help with rescue efforts.

### Built With

Project is built using the Python language for automation.
Satellite and Digit Elevation Models are processed and created by Mapbox. FFmpeg is used to generate a Video from the images.

* [Python](https://www.python.org)
* [Mapbox](https://www.mapbox.com)
* [FFmpeg](https://www.ffmpeg.org)



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Python 3

  ```sh
  brew install python
  ```

FFmpeg

  ```sh
  brew install ffmpeg
  ```

### Installation

1. Create an account and get a free API Key at [Mapbox](https://www.mapbox.com)
2. Replace  ```ENTER TOKEN``` with your api key, lines 54 & 60


<!-- USAGE EXAMPLES -->
## Usage

The Python script requires one argument, pass in the Coordinates of the area you would like to simulate.

  ```sh
  python3 main.py 35.686055952659096 139.75452642432558
  ```

After completion of the process, run FFmpeg to generate a video.

```sh
  ffmpeg  -i ./depth/%04d.png -c:v libx264 -c:a aac -ar 44100 -filter:v scale=1080:-1 -pix_fmt yuv420p output3.mp4
  ```

_For more examples, please refer to the [Documentation](https://example.com)_

## Clean up

Run the following commands to clean up before the next processing.

```sh
rm -rf ./satellite_images/*
  ```

```sh
rm -rf ./elevation_images/*
```

```sh
rm -rf ./composite_images/*
```

```sh
rm -rf ./depth/*
```

```sh
rm ./elevation.json
```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Your Name - [@adamgoodapp](https://twitter.com/adamgoodapp)

Project Link: [https://github.com/AdamGoodApp/Flood-sim](https://github.com/AdamGoodApp/Flood-sim)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/AdamGoodApp/Flood-sim/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/AdamGoodApp/Flood-sim/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/AdamGoodApp/Flood-sim/blob/main/LICENSE