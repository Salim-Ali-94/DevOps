#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(clippy::needless_return)]
#![allow(clippy::type_complexity)]
use std::collections::HashMap;


pub fn findInterval(function: fn(f64) -> f64, window: [f64; 2]) -> Vec<HashMap<String, f64>> {

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