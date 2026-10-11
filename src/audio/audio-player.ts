/**
 * Player class for decoding base64 audio strings. HEAVILY based on code by Arrow that can be found
 * here: https://www.khanacademy.org/computer-programming/i/5424847674523648
 */
export class AudioPlayer {
    // SO MANY FIELDS...can you tell I've been writing lots of C# lately?
    public get volume() {
        return this.gainNode.gain.value;
    }
    public set volume(value: number) {
        this.gainNode.gain.value = value;
    }

    public get playbackRate() {
        return this.source.playbackRate.value;
    }
    public set playbackRate(value: number) {
        this.source.playbackRate.value = value;
    }

    private _playing = false;
    public get playing() {
        return this._playing;
    }

    public get currentTime() {
        return this.audioContext.currentTime - this.startTime;
    }
    public set currentTime(value: number) {
        this.pauseTime = Math.min(Math.max(value, 0), this.duration);
    }

    public get loop() {
        return this.source.loop;
    }
    public set loop(value: boolean) {
        this.source.loop = value;
    }

    public get duration() {
        return this.buffer.duration;
    }

    private audioString: string;
    private audioContext: AudioContext;
    private buffer: globalThis.AudioBuffer
    private gainNode: GainNode;
    private source: AudioBufferSourceNode;

    private startTime: number;
    private pauseTime: number;

    /**
     * Creates a new audio player and initializes it with a base64 audio string.
     */
    public static async CreatePlayer(audioString: string): Promise<AudioPlayer> | null {
        const player = new AudioPlayer();
        try {
            await player.init(audioString);
            return player;
        }
        catch (e) {
            console.error(`Error while loading audio: ${e}`);
            return null;
        }
    }

    private constructor() {
        this.audioContext = new AudioContext();
        this.gainNode = this.audioContext.createGain();
        this.gainNode.connect(this.audioContext.destination);
    }

    /**
     * Loads an audio buffer string.
     */
    private async init(audioString: string) {
        this.audioString = audioString;
        await this.initBuffer();
    }

    public play() {
        if (this.audioContext.state === "suspended") {
            this.audioContext.resume();
        }
        this.createSource();
        this.source.start(this.startTime, this.pauseTime);
        this.startTime = this.audioContext.currentTime - this.pauseTime;
        this._playing = true;
    }

    public pause() {
        if (this.source) {
            this.source.stop();
            this.pauseTime = this.audioContext.currentTime - this.startTime;
            this._playing = false;
        }
    }

    public togglePlayPause() {
        if (this.playing) {
            this.pause();
        }
        else {
            this.play();
        }
    }

    private async initBuffer() {
        const binaryString = atob(this.audioString.split(',')[1]);
        const bytes = Uint8Array.from(binaryString, c => c.charCodeAt(0));
        this.buffer = await this.audioContext.decodeAudioData(bytes.buffer);
    }

    private createSource() {
        this.source = this.audioContext.createBufferSource();
        this.source.buffer = this.buffer;
        this.source.connect(this.gainNode);
    }
}