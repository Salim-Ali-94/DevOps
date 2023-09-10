#![allow(non_snake_case)]
#![allow(clippy::needless_return)]
#![allow(clippy::type_complexity)]
#![allow(unused_parens)]
use rand::Rng;


pub fn rsaPublicKeyGenerator(maximum: u64) -> (u64, u64) {

	let mut primes = sieveOfEratosthanes(maximum);
	let mut rng = rand::thread_rng();
	let index_p = rng.gen_range(0..primes.len());
	primes.remove(index_p);
	let index_q = rng.gen_range(0..primes.len());
	let p = primes[index_p];
	let q = primes[index_q];
	let n = p*q;
	let phi = (p - 1)*(q - 1);
	primes.push(p);
	return (phi, n);

}

fn sieveOfEratosthanes(maximum: u64) -> Vec<u64> {

	let sieve: Vec<u64> = (2..=maximum).collect();
	let mut primes = sieve.clone();

	for check in 2..=(maximum as f64).sqrt().floor() as u64 {

		let index = sieve.iter().position(|&value| value == check).unwrap();

		for number in sieve[index + 1..].iter() {

			if (primes.contains(number) && (*number % check == 0)) {

				let delete = primes.iter().position(|value| *value == *number).unwrap();
				primes.remove(delete);

			}

		}

	}

	return primes;

}
