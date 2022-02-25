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
and enter the animation number you want to see (does not show brightness changes)
