#![allow(non_snake_case)]
#![allow(clippy::needless_return)]
#![allow(clippy::type_complexity)]
#![allow(unused_parens)]
use rand::Rng;


pub fn rsaPublicKeyGenerator(maximum: u128) -> (u128, u128, u128, u128, u128) {

	let mut primes = sieveOfEratosthanes(maximum);
	let mut rng = rand::thread_rng();
	let index_p = rng.gen_range(0..primes.len());
	let p = primes[index_p];
	primes.remove(index_p);
	let index_q = rng.gen_range(0..primes.len());
	let q = primes[index_q];
	let n = p*q;
	let phi = (p - 1)*(q - 1);
	primes = sieveOfEratosthanes(phi);
	// primes.sort_by(|a, b| b.cmp(a));
	let mut e = 0;

	if (primes[primes.len() - 1] == phi) {

		primes.remove(primes.len() - 1);

	}

	if (primes.len() > 3) {

		for constant in [p, q, n].iter() {

			if primes.contains(constant) {

				primes.retain(|&value| value != *constant);

			}
		
		}

	}

	for prime in primes.iter() {

		let gcd = euclideanAlgorithm(*prime, phi);

		if (gcd == 1) {

			e = *prime;
			break;

		}

	}

	if (e == 0) {

		let last = primes[primes.len() - 1];
		primes = sieveOfEratosthanes(last + 50);

		if (primes.len() > 1) {

			let index = primes.iter().position(|&value| value == last).unwrap();

			for prime in primes[index..].iter() {

				let gcd = euclideanAlgorithm(*prime, phi);

				if (gcd == 1) {

					e = *prime;
					break;

				}

			}

		}

	}

	return (p, q, n, phi, e);

}

fn sieveOfEratosthanes(maximum: u128) -> Vec<u128> {

	let sieve: Vec<u128> = (2..=maximum).collect();
	let mut primes = sieve.clone();

	for check in 2..=(maximum as f64).sqrt().floor() as u128 {

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

fn euclideanAlgorithm(mut a: u128, mut b: u128) -> u128 {

	if (a < b) {

		let c = a;
		a = b;
		b = c;

	}

	while (a % b != 0) {

		let c = a % b;
		a = b;
		b = c;

	}

	return b;

}
