declare module "*" {
    import * as p5 from "p5";
    global {
        type p5 = p5.default;
    }
}