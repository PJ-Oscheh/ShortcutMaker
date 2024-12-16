# Shortcut Maker

Easily create shortcuts on the GNOME desktop

<p align="center">
  <img src=./data/icons/io.github.pj_oscheh.shortcutmaker.svg width=256 height=256/>
</p>

<p align="center">
  <img src=https://github.com/user-attachments/assets/f541e31e-a9c6-4235-8e84-f516f0382e0c />
</p>

Ever come across a stubborn one-off app that REFUSES to ship as anything but a stand-alone binary? You know the one. Often times, these apps won't come with an install script (at least, one that creates a proper desktop icon!). For these apps,
let Shortcut Maker come to the rescue. It simplifies the process of creating a `.destkop` file by guiding the user through the shortcut creation process.

Currently, the application supports:
- Naming the shortcut (`Name`)
- Setting the executable path (`Exec`)
- Setting the icon (`Icon`)
- Specifying whether the terminal should be used (`Terminal`)
- Setting comments (`Comment`)
- Specifying categories (although without any fancy front-end; just as a string) (`Categories`)

This app creates `.desktop` files according to the [FreeDesktop Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/latest/). While this app should work fine on KDE and other desktop environments
that follow these specifications, I haven't tested those environments.

Stack:
- UI Toolkit: GTK 4 and Adwaita
- Language: Python
