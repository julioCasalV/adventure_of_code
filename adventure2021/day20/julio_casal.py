import numpy as np
import time

decode = np.loadtxt('input.txt', max_rows=1, comments='t', dtype='str')
image_orig = np.loadtxt('input.txt', skiprows=1, comments='t', dtype='str')
decode = str(decode)
decode = decode.replace("#", "1")
decode = decode.replace(".", "0")
decode = [int(i) for i in decode]

image_orig = np.char.replace(image_orig, "#", "1")
image_orig = np.char.replace(image_orig, ".", "0")
list_point_tmp = []
for item in image_orig:
    list_point_tmp.append(list(item))


image_orig = np.array(list_point_tmp).reshape(len(image_orig), -1).astype(int)
pad = 105
image_orig = np.pad(image_orig, ((pad, pad), (pad, pad)), 'constant', constant_values=0)

iterations = 50
for repeat in range(iterations):
    image_orig_new = image_orig.copy()
    for (idx, idy), x in np.ndenumerate(image_orig[:-1,:-1]):
        ref = image_orig[idx:idx+3, idy:idy+3].reshape(-1)
        ref = "".join(ref.astype('str'))
        ref = int(ref, 2)
        image_orig_new[idx+1, idy+1] = decode[ref]
    image_orig = image_orig_new.copy()

pad = 52
image_orig = image_orig[pad:-pad, pad:-pad]

print(image_orig)
print(np.sum(np.sum(image_orig)))

    