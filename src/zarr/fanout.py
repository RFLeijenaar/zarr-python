from zarr.core.chunk_key_encodings import ChunkKeyEncoding


class FanoutChunkKeyEncoding(ChunkKeyEncoding):
    name = "fanout"

    def decode_chunk_key(self, chunk_key: str) -> tuple[int, ...]:
        if chunk_key == "c":
            return ()
        return tuple(map(int, chunk_key[1:].split(self.separator)))

    def encode_chunk_key(self, chunk_coords: tuple[int, ...]) -> str:
        return self.separator.join(map(str, ("c",) + chunk_coords))