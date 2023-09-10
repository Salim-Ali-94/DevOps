#![allow(non_snake_case)]
#![allow(clippy::needless_return)]
#![allow(clippy::type_complexity)]
#![allow(unused_parens)]
use rand::Rng;


pub fn rsaKeyGenerator(maximum: u64) -> (u64, u64) {

	let primes = sieveOfEratosthanes(maximum);
	let mut rng = rand::thread_rng();
	let index_p = rng.gen_range(0..primes.len());
	let mut index_q = rng.gen_range(0..primes.len());
	index_q = index_p;

	while (index_q == index_p) {

		index_q = rng.gen_range(0..primes.len());

	}

	let p = primes[index_p];
	let q = primes[index_q];
	let n = p*q;
	let phi = (p - 1)*(q - 1);
	return (phi, n)

}

fn sieveOfEratosthanes(maximum: u64) -> Vec<u64> {

	let mut sieve = vec![];
	// let mut primes = vec![];

	for integer in 2..=maximum {

		sieve.push(integer);

	}

	let mut primes = sieve.clone();

	// for check in 2..=sqrt(maximum as f64).floor() as usize {
	for check in 2..=(maximum as f64).sqrt().floor() as u64 {
	// for check in 2..=num::sqrt(maximum as f64).floor() as usize {

		let index = sieve.iter().position(|&value| value == check).unwrap();
		// let range = index..sieve.len();

		// for number in &sieve[index..sieve.len()].iter_mut() {

		// for number in sieve[index..sieve.len()].iter_mut() {
		// for number in sieve[range] {
		for number in sieve[index..].iter() {

		// for number in sieve[index..sieve.len()] {

			// // if (number % check == 0) {
			// if (*number % check == 0) {

			// 	// let delete = sieve.iter().position(|value| *value == number).unwrap();
			// 	let delete = sieve.iter().position(|value| *value == *number).unwrap();
			// 	sieve.remove(delete);

			// }

			// // if (number % check == 0) {
			// if (*number % check == 0) {

			// 	if primes.contains(number) {

			// 		// let delete = sieve.iter().position(|value| *value == number).unwrap();
			// 		let delete = primes.iter().position(|value| *value == *number).unwrap();
			// 		primes.remove(delete);

			// 	}

			// }

			// if primes.contains(number) {

			// 	if (*number % check == 0) {

			// 		let delete = primes.iter().position(|value| *value == *number).unwrap();
			// 		primes.remove(delete);

			// 	}

			// }

			if (primes.contains(number) && (*number % check == 0)) {

				let delete = primes.iter().position(|value| *value == *number).unwrap();
				primes.remove(delete);

			}

			// else {

			// 	if !primes.contains(number) {


			// 	}

			// }

		}

	}

	// return sieve
	return primes

}
