# Genetic Bike:
This repository shows how to optimize the designs of a simplified bike using
an evolutionary algorithm.

## Usage:
### import libraries
```
from floor import Floor
from bike  import Bike
import numpy as np
from solver import Euler as run
from score import score
from evol import next_gen
```

### Create a track and a first generation of bikes
```
ground = Floor()
bike_list = [Bike() for _ in range(100)]
```

### Let the bikes run through the track
```
for bike in bike_list:
    run(bike, ground)
    score(bike)
# sort bike list by by score
bike_list.sort(key=lambda x: x.score, reverse=True)
```

### Selection + mutations and crossovers create the new bike generation
```
bike_list = next_gen(bike_list,n_crosses=50,n_mutations=50)
# let's run the new bikes through the path and rank them
for bike in bike_list:
    run(bike, ground)
    score(bike)
bike_list.sort(key=lambda x: x.score, reverse=True)
```

### Animation
```
from animation import Render
import matplotlib.pyplot as plt
import matplotlib.animation as animation
ibike = 0 # bike number, from 0 to len(bike_list)-1
render = Render(ground, bike_list[ibike], ibike)
ani = animation.FuncAnimation(render.fig, render.animate, init_func = render.init_line, frames = render.nframes, interval = 0.0, repeat = False, blit = True)
plt.show()
```
