<h1 align="center">Hi, welcome to Easy Game with Python ! 🔥🔥🔥</h1>

<h2 align="center">🎮 A couple of introductions 🎮</h2>
<img align="right" src="Image/icon.png">

```python
print('Hello there, I am Fish. :3')
print('I enjoy programming, particularly in data structures, algorithms, and game development')
print('Now, let me introduce you to my project. <3')

objective = {
	'overview': 'easy to use',
	'community': 'easy to share source code',
	'optimization': 'high reusability, source code optimization'
}
print('Our goal is to provide a powerful Python library for game development :',
	objective, sep='\n')

knowledge = {
	'programming language': 'basic understanding of Python',
	'level': 'be able to read and comprehend documentation',
	'library': 'know how to use the Pygame and Numpy libraries'
}
print('Before you start using it, you should have :', knowledge, sep='\n')

if __name__ == '__main__':
	print('Welcome to our pygamesupporter package !')
```

### Before you continue, ensure you meet the following requirements
* You have installed the **pygame**, **numpy** package 📦.
* You have a basic understanding of *python syntax*, *Object Oriented Programing of python* and *pygame package* 🎮.
* You have installed the **pygamesupporter** package in this repository 🎲.

## <h1 align="center">⛓️ Install package ⛓️</h1>

- Download the **pygamesupporter** folder ( **pygamesupporter** package ), put them in the same folder of the project.

## <h1 align="center">Quick introduction</h1>

> Introduces powerful features in the **pygamesupporter** package.

<details>
<summary><h3>About: <i>Pygame wrapper</i></h3></summary>
<br>

The `pygamesupporter` package provides a `pygame` wrapper to handle events that occur within the game. You will indirectly use `pygame` methods through classes provided by `pygamesupporter`, or use them directly on `pygame`.
- With this package, you can easily handle and manipulate mouse and keyboard events to interact with the game. Additionally, it also allows you to draw mouse cursor icons using external images or default icons.
- It provides variables related to time such as delta time and fps. This makes handling real-time events and displaying the game's FPS a breeze. In fact, you can even create your own FPS game.
</details>

---
<details>
<summary><h3>About: <i>Each scene in one class</i></h3></summary>
<br>

<i>Each scene in the game is written separately in a separate class</i>, making it easier for you to focus on managing a scene efficiently.<br>

Moreover, `pygamesupporter` <i>allows you to easily share data between different scenes</i>. This feature allows you <i>to reuse controls from another scene without having to create them again</i>, reducing the user's wait time when switching scenes and providing the best possible user experience.

In other words, with `pygamesupporter`, organizing and managing game scenes has never been easier ! Try it out for yourself and see the difference.
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
