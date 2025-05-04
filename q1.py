from hashlib import sha512

import multiprocessing as mp
import time

WORDS = ['extra-large', 'invincible', 'furtive', 'stare', 'ruddy', 'adaptable', 'daily', 'letters', 'houses', 'grate', 'fog', 'stupendous']

def hash(word: str):
    hash_object = sha512()
    for _ in range(100):
        time.sleep(.01)
        byte_data = word.encode('utf-8')
        hash_object.update(byte_data)
        word = hash_object.hexdigest()
    return word

def main():
    start_time = time.time()
    
    with mp.Pool() as pool:
        results = []
        
        for word in WORDS:
            result = pool.apply_async(hash, args=(word,))
            results.append(result)
        
        for result in results:
            print(result.get())
    
    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    main()