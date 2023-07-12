#![allow(non_snake_case)]
use rand::Rng;


pub fn aesKeyGenerator(mut key_length: i32) -> (String, i32) {

	let mut rounds = 0;

	if key_length <= 128 {

		key_length = 128;
		rounds = 10;

	} else if key_length > 128 && key_length <= 192 {

		key_length = 192;
		rounds = 12;

	} else if key_length >= 256 {

		key_length = 256;
		rounds = 14;

	}

	let mut rng = rand::thread_rng();
	let x = rng.gen_range(1..=100);
	println!("aes key: {}", x);
	println!("aes key length: {}", key_length);
	println!("aes number of rounds: {}", rounds);
	return (key_length.to_string(), rounds);

}