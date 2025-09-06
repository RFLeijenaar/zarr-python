from pathlib import Path

import numpy as np

import zarr
import zarr.codecs
from zarr.core.chunk_key_encodings import ChunkKeyEncoding
from zarr.registry import register_chunk_key_encoding
from zarr.storage import LocalStore, WrapperStore
# from numcodecs.zarr3 import


class FanoutStore(WrapperStore):
    pass


class FanoutChunkKeyEncoding(ChunkKeyEncoding):
    name = "fanout"

    def decode_chunk_key(self, chunk_key: str) -> tuple[int, ...]:
        if chunk_key == "c":
            return ()
        return tuple(map(int, chunk_key[1:].split(self.separator)))

    def encode_chunk_key(self, chunk_coords: tuple[int, ...]) -> str:
        return self.separator.join(map(str, ("c",) + chunk_coords))

register_chunk_key_encoding("fanout", FanoutChunkKeyEncoding)


def main():
    store = Path("~/data/test.zarr").expanduser()
    store = FanoutStore(LocalStore(store))

    # z = zarr.open_array(store)

    z = zarr.create_array(
        store,
        shape=(100_000, 3),
        # shards=(1_000_000, 3),
        chunks=(1_000, 3),
        dtype=np.uint16,
        chunk_key_encoding={"name": "v2"},
        # chunk_key_encoding=FanoutChunkKeyEncoding(separator="/"),
        # chunk_key_encoding="fanout",
        overwrite=True,
        # compressors=zarr.codecs.BloscCodec(),
        # compressors=GZip(),
    )
    rng = np.random.default_rng()
    data = rng.integers(0, 65_535, size=(10_000_000, 3), dtype=np.uint16)
    z[:] = data
    print(z.info)


if __name__ == "__main__":
    main()
