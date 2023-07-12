#![allow(non_snake_case)]
use rand::Rng;


pub fn aesKeyGenerator() {

	let mut rng = rand::thread_rng();
	let x = rng.gen_range(1..=100);
	println!("aes key: {}", x);

}