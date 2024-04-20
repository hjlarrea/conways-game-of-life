# Positional, coordinates and array equivalences

During the development process I noticed a number of confusions that happened in terms of how to map my mental model, to the logical distribution of the array to the graphics on the screen. Therefore I created this table to remain aware on how these three are mapped together:

|Element|X|Y|
|-|-|-|
|Concept| Column | Row |
|Variables| col | row |
|Loop Indexes| j | i |
|`pos` tuple | `pos[0]` | `pos[1]` |

### Things to take into account

The two dimensional array is organized as this:

```python
[
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]
]
```

In this context it is normal to think about loops arranged like this:

```python
for i in range(0,BOARDSIZE):
    for j in range(0,BOARDSIZE):
        pass
```

It is normal to think `x,y` coordinates map to `i,j`, but it's the opossite, as the slowest loop `i` will iterate over the rows (`y`) and the fastest loop `j` will iterate over the columns (`x`).

For list comprenhensions this should be:

```python
[[pass for j in range(0,BOARDSIZE)] for i in BOARDSIZE]
```