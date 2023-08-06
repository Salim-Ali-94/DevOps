#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(clippy::needless_return)]
#![allow(clippy::type_complexity)]
use std::collections::HashMap;


pub fn secant(function: fn(f64) -> f64, window: [f64; 2], precision: f64) -> (Vec<f64>, f64, u64) {

	let mut roots = vec![];
	let mut iterations: u64 = 0;
	let mut residual: f64 = 0.0;
	let intervals = findInterval(function, window);

	for interval in intervals.iter() {

		let mut x0 = *interval.get("lower").unwrap();
		let mut x1 = *interval.get("upper").unwrap();
		residual = 2.0*precision;

		while (residual.abs() > precision) {

			let x = x1 - function(x1)*(x1 - x0) / (function(x1) - function(x0));
			residual = (x - x1) / x;
			iterations += 1;
			x0 = x1;
			x1 = x;

			if (residual.abs() < precision) {

				roots.push(x);

			}

		}

	}

	return (roots, residual, iterations);

}

fn findInterval(function: fn(f64) -> f64, window: [f64; 2]) -> Vec<HashMap<String, f64>> {

	let mut domain: Vec<HashMap<String, f64>> = Vec::new();
	let mut interval: HashMap<String, f64> = HashMap::new();
	let mut initial: f64 = window[0];
	let width: f64 = (window[1] - initial).abs();
	let mut step: f64 = 1.0;
	let mut delta = width / step;
	let mut x: f64 = initial;

	while (delta > 1.0) {

		step += 1.0;
		delta = width / step;
	
	}

	while (x < window[1]) {

		x += delta;

		if (function(initial)*function(x) < 0.0) {

			interval.insert("lower".to_string(), initial);
			interval.insert("upper".to_string(), x);
			domain.push(interval.clone());

		}

		initial = x

	}

	return domain;

}
