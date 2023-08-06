#![allow(non_snake_case)]
#![allow(clippy::needless_return)]
#![allow(clippy::type_complexity)]
use std::collections::HashMap;


pub fn findInterval(function: fn(f64) -> f64, window: [f64; 2]) -> Vec<HashMap<String, f64>> {

    let mut domain: Vec<HashMap<String, f64>> = Vec::new();
    let mut interval: HashMap<String, f64> = HashMap::new();
    interval.insert("minimum".to_string(), -100.0);
    interval.insert("maximum".to_string(), 100.0);
    domain.push(interval);
    return domain;

}