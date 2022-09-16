code i wrote for tyler jackson's monolith works

couldnt find a tonne of examples for rpi_ws281x on raspberry pi so hopefully this helps
someone in the future. it is pretty naive but works well enough.

made to be run on raspberry pi, the program cant be run locally. i use balena because i dont have 
physical access to the device but i dont think it matters.

run tests:
```
cd src
python -m unittest discover -s tests -p "*_test.py"
```

 🤙

locally preview led animations:
```
python src/animatetools.py
```
and enter the animation number you want to see

please note that the speed of the animation does not reflect reality.
the leds are extremely slow.
the less changes per cycle the faster they are. for example to make things like gradients faster,
you can reduce the number of different colours in them by chunking colours every n-th led (what i was planning on doing next).
figuring out if there is a bottleneck somewhere that is causing the speed problems would make the biggest impact.
