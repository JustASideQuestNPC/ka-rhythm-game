import p5 from "p5";

// collect and delete existing animation frames
for(let i = window.requestAnimationFrame(() => {}); i > 0; i--) {
    window.cancelAnimationFrame(i);
}

// creates and runs the actual sketch object
const sketch = (p5: p5) => {
    p5.setup = () => {
        const canvas = p5.createCanvas(600, 600);

        // i already have a reference to the canvas that i got from the canvas parameter, and i can
        // use that to make mouse functions only trigger when the mouse is over the canvas, but if i
        // do that then it just casually doesn't pass an event to mousePressed???? so now i have to
        // use this to get a DIFFERENT reference to the SAME THING just to fix that. I SHOULD NOT
        // HAVE TO DO ANY OF THIS DO YOU REALIZE HOW LONG IT TOOK ME TO FIND THIS BUG
        const c = document.getElementById(canvas.id()) as HTMLElement;

        // makes keyboard functions only work when the canvas has focus (and makes the debug console
        // hotkey still work)
        c.tabIndex = -1;
        c.addEventListener("mousedown", mousePressed);
        c.addEventListener("mouseup", mouseReleased);
        c.addEventListener("keydown", keyPressed);
        c.addEventListener("keyup", keyReleased);
        // disables the right-click menu
        c.addEventListener("contextmenu", (e) => e.preventDefault());
    };

    p5.draw = () => {
        p5.background("#e0e0e0");
    };

    function keyPressed(event: KeyboardEvent) {
        console.log(event);
    }

    function keyReleased(event: KeyboardEvent) {
        console.log(event);
    }

    function mousePressed(event: MouseEvent) {
        console.log(event);
    }
    
    function mouseReleased(event: MouseEvent) {
        console.log(event);
    }
};

// error checks need to be disabled here because otherwise typescript explodes for some reason
// @ts-ignore
const instance = new p5(sketch);