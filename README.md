<h1 align="center">Hi, welcome to Easy Game with Python ! 🔥🔥🔥</h1>

<h2 align="center">🎮 About me 🎮</h2>
<img align="right" src="Image/icon.png">

```python
information = {
	'nickname': 'Fish',
	'education': 'University',
	'code': ['Python', 'C++', 'C#'],
	'favourite': ['Data Structure', 'Code game', 'Configuration']
}

about_repository = {
	'objective': 'Provide game programming library',
	'language': 'Python',
	'level': ['Basic', 'Reading comprehension', 'Apply']
}

if __name__ == '__main__':
	library_use = 'pygame'
```

### Before you continue, ensure you meet the following requirements
* You have installed the *pygame* package 📦.
* You have a basic understanding of *python syntax*, *OOP of python* and *pygame* 🎮.
* You have installed the *speedgame* package in this repository 🎲.

## <h1 align="center">⛓️ Install package ⛓️</h1>

- Download the *speedgame* folder ( *speedgame* package ), put them in the same folder of the project.

## <h1 align="center">Quick introduction</h1>

> Introduce the modules of the package.

<details>
<summary><h3>About module <i>Handle</i></h3></summary>
<br>

Name | Type | Feature |
:---: | :---: | ---
`GameHandle` | Class SingletonMeta | Class with application program management functionality.
`app` | Variable | Instance of `GameHandle`, pre-initialized for use as a *global variable*.
`app.cursor` | Variable | Instance of `CursorHandle`, used to get mouse information, events.
`app.time` | Variable | Instance of `TimeHandle`, used to get the interval between two consecutive frames.

</details>

---
<details>
<summary><h3>About module <i>Basic</i></h3></summary>
<br>

Name | Type | Feature |
:---: | :---: | ---
`Color` | Static Class | `Color` defines default colors.
`Math` | Static Class | `Math` defines basic calculation functions.
`Vector2` | Class | Support calculations with vectors in the plane.
`icon` | Variable | The global variable `icon` is used to load icons in the `InterfaceIcons` directory.
`font` | Variable | The global variable `font` is used to load fonts in the `InterfaceFonts` directory.

</details>

---
<details>
<summary><h3>About module <i>Surface</i></h3></summary>
<br>

Name | Type | Feature |
:---: | :---: | ---
`ImageProcessor` | Static Class | `ImageProcessor` provides methods for processing images.
`Image` | Class | Save an image, coordinates, size of the image, ... .
`Label` | Class | Save and image of label, title, position, size of image, ... .
`FPSLabel` | Class | Show the number of frames per second, it will change every millisecond `time_wait`.
`CursorImage` | Class | Save icons of cursor.
`CursorShoot` | Class | Save icons of cursor.

</details>

---
<details>
<summary><h3>About module <i>Control</i></h3></summary>
<br>

Name | Type | Feature |
:---: | :---: | ---
`Control` | Abstract Class | Interface for control classes.
`Button` | Abstract Class | Interface for *button* classes.
`ImageControl` | Class | Image class has additional events.
`ButtonBoostrap` | Class | Button class simulates **Bootstrap**.
`ButtonImage` | Class | `ButtonImage` class takes image as a button.
`PickPopEvent` | Class | Simulate surface drag and drop event.

</details>

---
<details>
<summary><h3>About module <i>Controller</i></h3></summary>
<br>

Name | Type | Feature |
:---: | :---: | ---
`ExistenceController` | Class | `ExistenceController` class support initial, destroy game objects.
`SceneController` | Class SingletonMeta | The `SceneController` class supports the management of scenes.
`LayerController` | Class | The `LayerController` support the management of layers.

</details>

## <h1 align="center">🔥 Tutorial 🔥</h1>

> You should study the items in turn in the order below. 🥇

<details>
<summary><h3>🎮 Variable name <i>'app'</i></h3></summary>
<br>
Well, you will learn it !
</details>

---
<details>
<summary><h3>🎮 Variable name <i>'icon'</i>, <i>'font'</i></h3></summary>
<br>
Well, you will learn it !
</details>

---
<details>
<summary><h3>🎮 <i>Image</i> and <i>Label</i></h3></summary>
<br>
Well, you will learn it !
</details>
