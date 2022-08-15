# Maze

https://user-images.githubusercontent.com/7283624/183983986-626d8a34-1e45-40c2-af9a-79ddd010a31a.mp4


To understand how these Mazes are constructed, watch the accompanying [⏵︎video tutorials](https://www.youtube.com/watch?v=d5yzKkG1n1U&list=PLUNDATSEu7fiBiwCEkXr_ncDGYQMkoevr).

## Quick Start
No installations required. Just clone this repository and run code

```bash
$ git clone https://github.com/emadehsan/maze

$ cd maze/src

# draw a rectangular maze
$ python rectangular.py

# or a circular maze
$ python circular.py

# or a triangular maze
$ python triangular.py

# or a hexagonal maze
$ python hexagonal.py
```

## Current Mazes
* **Rectangular Maze** using Randomized Prim's Algorithm [ [tutorial](https://www.youtube.com/watch?v=d5yzKkG1n1U) ]

    <img src="./media/squared.png" alt="Squared Maze using Prims Algorithm" width="300"/>


* **Circular Maze** using Depth First Search [ [tutorial](https://www.youtube.com/watch?v=q7t8UVlu-Fk) ]
    
    <img src="./media/circular.png" alt="Circular Maze using Depth First Search" width="300"/>

* **Triangular Maze** using Depth First Search

    <img src="./media/triangular.PNG" alt="Triangular Maze using Depth First Search" width="300"/>

* **Triangular Maze** using Kruskal's Algorithm 
    
    <img src="./media/triangular_kruskal.PNG" alt="Triangular Maze using Kruskal Algorithm" width="300"/>

* **Hexagonal Maze** using Depth First Search 

    <img src="./media/hexagonal.PNG" alt="Hexagonal Maze using Depth First Search" width="300"/>

## Generate Maze Dataset
You can also generate a dataset of Mazes. Right now, only Rectangular 
(actually Squared) Mazes are supported. 

Use the scripts in [`src/datasets`](src/datasets).