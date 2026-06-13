import numpy as np
from PIL import Image
import random
import math
def get_image_metadata(path):
    img = Image.open(path)
    return {
        'width': img.width,
        'height': img.height,
        'mode': img.mode,
        'format': img.format or 'PNG'
    }
# ─────────────────────────────────────────────
# 1. XOR ENCRYPTION
# ─────────────────────────────────────────────
def xor_encrypt(input_path, output_path, key):
    img = Image.open(input_path).convert('RGB')
    pixels = np.array(img, dtype=np.uint8)
    encrypted = pixels ^ key
    Image.fromarray(encrypted.astype(np.uint8)).save(output_path)
def xor_decrypt(input_path, output_path, key):
    # XOR is symmetric — same operation decrypts
    xor_encrypt(input_path, output_path, key)
# ─────────────────────────────────────────────
# 2. PIXEL SWAP ENCRYPTION
# ─────────────────────────────────────────────
def pixel_swap_encrypt(input_path, output_path, key):
    img = Image.open(input_path).convert('RGB')
    pixels = np.array(img, dtype=np.uint8)
    h, w, c = pixels.shape
    flat = pixels.reshape(-1, c)
    indices = list(range(len(flat)))
    rng = random.Random(key)
    rng.shuffle(indices)
    shuffled = flat[indices]
    result = shuffled.reshape(h, w, c)
    Image.fromarray(result.astype(np.uint8)).save(output_path)
def pixel_swap_decrypt(input_path, output_path, key):
    img = Image.open(input_path).convert('RGB')
    pixels = np.array(img, dtype=np.uint8)
    h, w, c = pixels.shape
    flat = pixels.reshape(-1, c)
    indices = list(range(len(flat)))
    rng = random.Random(key)
    rng.shuffle(indices)
    reverse_indices = [0] * len(indices)
    for i, idx in enumerate(indices):
        reverse_indices[idx] = i
    restored = flat[reverse_indices]
    result = restored.reshape(h, w, c)
    Image.fromarray(result.astype(np.uint8)).save(output_path)
# ─────────────────────────────────────────────
# 3. MATHEMATICAL OPERATION ENCRYPTION
# ─────────────────────────────────────────────
def math_operation_encrypt(input_path, output_path, key, operation='add'):
    img = Image.open(input_path).convert('RGB')
    pixels = np.array(img, dtype=np.int32)
    if operation == 'add':
        result = (pixels + key) % 256
    elif operation == 'subtract':
        result = (pixels - key) % 256
    elif operation == 'multiply':
        result = (pixels * key) % 256
    elif operation == 'bitwise_and':
        result = pixels & key
    elif operation == 'bitwise_or':
        result = pixels | key
    else:
        result = (pixels + key) % 256
    Image.fromarray(result.astype(np.uint8)).save(output_path)
def math_operation_decrypt(input_path, output_path, key, operation='add'):
    img = Image.open(input_path).convert('RGB')
    pixels = np.array(img, dtype=np.int32)
    if operation == 'add':
        result = (pixels - key) % 256
    elif operation == 'subtract':
        result = (pixels + key) % 256
    elif operation == 'multiply':
        # Find modular inverse if possible
        try:
            inv = pow(int(key), -1, 256)
            result = (pixels * inv) % 256
        except Exception:
            result = pixels
    elif operation == 'bitwise_and':
        result = pixels | (~key & 0xFF)
    elif operation == 'bitwise_or':
        result = pixels & (~key & 0xFF)
    else:
        result = (pixels - key) % 256
    Image.fromarray(result.astype(np.uint8)).save(output_path)
# ─────────────────────────────────────────────
# 4. CHANNEL SHIFT ENCRYPTION
# ─────────────────────────────────────────────
def channel_shift_encrypt(input_path, output_path, key):
    img = Image.open(input_path).convert('RGB')
    pixels = np.array(img, dtype=np.uint8)
    r, g, b = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
    shift = key % 3
    if shift == 0:
        new_r, new_g, new_b = g, b, r
    elif shift == 1:
        new_r, new_g, new_b = b, r, g
    else:
        new_r, new_g, new_b = g, r, b
    # Also shift values within channels
    new_r = (new_r.astype(np.int32) + key) % 256
    new_g = (new_g.astype(np.int32) + (key * 2)) % 256
    new_b = (new_b.astype(np.int32) + (key * 3)) % 256
    result = np.stack([new_r, new_g, new_b], axis=2).astype(np.uint8)
    Image.fromarray(result).save(output_path)
def channel_shift_decrypt(input_path, output_path, key):
    img = Image.open(input_path).convert('RGB')
    pixels = np.array(img, dtype=np.int32)
    r, g, b = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
    # Reverse value shift
    r_unshifted = (r - key) % 256
    g_unshifted = (g - key * 2) % 256
    b_unshifted = (b - key * 3) % 256
    shift = key % 3
    if shift == 0:
        orig_r, orig_g, orig_b = b_unshifted, r_unshifted, g_unshifted
    elif shift == 1:
        orig_r, orig_g, orig_b = g_unshifted, b_unshifted, r_unshifted
    else:
        orig_r, orig_g, orig_b = g_unshifted, b_unshifted, r_unshifted  # g,r,b → r=g,g=r reversed
    result = np.stack([orig_r, orig_g, orig_b], axis=2).astype(np.uint8)
    Image.fromarray(result).save(output_path)
# ─────────────────────────────────────────────
# 5. ARNOLD CAT MAP ENCRYPTION
# ─────────────────────────────────────────────
def arnold_cat_map(pixels, iterations):
    """Apply Arnold's Cat Map to scramble pixel positions."""
    h, w = pixels.shape[:2]
    N = min(h, w)
    sq = pixels[:N, :N].copy()
    for _ in range(iterations):
        new_sq = np.zeros_like(sq)
        for y in range(N):
            for x in range(N):
                new_x = (x + y) % N
                new_y = (x + 2 * y) % N
                new_sq[new_y, new_x] = sq[y, x]
        sq = new_sq
    result = pixels.copy()
    result[:N, :N] = sq
    return result
def arnold_cat_map_inverse(pixels, iterations):
    """Apply inverse Arnold's Cat Map to restore pixel positions."""
    h, w = pixels.shape[:2]
    N = min(h, w)
    sq = pixels[:N, :N].copy()
    for _ in range(iterations):
        new_sq = np.zeros_like(sq)
        for y in range(N):
            for x in range(N):
                new_x = (2 * x - y) % N
                new_y = (-x + y) % N
                new_sq[new_y, new_x] = sq[y, x]
        sq = new_sq
    result = pixels.copy()
    result[:N, :N] = sq
    return result
def arnold_cat_map_encrypt(input_path, output_path, iterations=5):
    img = Image.open(input_path).convert('RGB')
    pixels = np.array(img, dtype=np.uint8)
    result = arnold_cat_map(pixels, iterations)
    Image.fromarray(result).save(output_path)
def arnold_cat_map_decrypt(input_path, output_path, iterations=5):
    img = Image.open(input_path).convert('RGB')
    pixels = np.array(img, dtype=np.uint8)
    result = arnold_cat_map_inverse(pixels, iterations)
    Image.fromarray(result).save(output_path)
