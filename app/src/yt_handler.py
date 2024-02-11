from pytube import YouTube


class yt_dl(YouTube):
    def __init__(self, url: str):
        super().__init__(url)

    def get_filtered_streams(self):
        self.filtered_streams = self.streams.filter(
            progressive="True", mime_type="video/mp4"
        )
        return self.filtered_streams

    def get_organized_options(self):
        y = []
        for stream in self.get_filtered_streams():
            y.append(
                {
                    "itag": f"{stream.itag}",
                    "res": f"{stream.resolution}",
                    "fps": f"{stream.fps}",
                }
            )
        return y


if __name__ == "__main__":
    ...