declare module "*" {
    import * as p5 from "p5";
    global {
        type p5 = p5.default;
        // stores base64 strings for all audio
        var AUDIO_STRINGS: { [key: string]: string };
    }
}