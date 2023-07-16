#![allow(non_snake_case)]
use rand::Rng;
pub mod constants;


pub fn aesKeyGenerator(aes_standard: i16) -> (String, Vec<Vec<String>>, i8) {

	let mut rng = rand::thread_rng();
	let mut key = if rng.gen_range(0.0..1.0) < 0.5 { "1".to_owned() } else { "0".to_string() };
	let rounds;
	let key_length;

	if aes_standard <= 128 {

		key_length = 128;
		rounds = 10;

	} else if aes_standard > 128 && aes_standard <= 192 {

		key_length = 192;
		rounds = 12;

	} else {

		key_length = 256;
		rounds = 14;

	}

	while key.len() < key_length as usize {

        if rng.gen_range(0.0..1.0) < 0.5 {

            key.push_str("1");

        } else {

            key.push_str("0");

        }
        
	}

	key = shuffleBits(key);
	let hex = stackBytes(key.clone());
	return (key, hex, rounds);

}

pub fn spliceDocument(file: String, chunk: i16) -> (String, Vec<Vec<Vec<String>>>) {

	let mut message = encodeDocument(file);
	let mut document = vec![];
	let mut buffer = vec![];
	let mut column = vec![];
	let mut block;

	while message.len() % (chunk as usize / 4) != 0 {

		message.push_str(&format!("{:02x}", b'~'));

	}

	for word in (0..message.len()).step_by((chunk as usize) / 4) {

		block = message[word..word + (chunk as usize) / 4].to_string();

		for character in (0..(chunk as usize) / 4).step_by(8 / 4) {
		
			column.push(block[character..character + 8 / 4].to_string());

			if column.len() == 4 {

				buffer.push(column.clone());
				column.clear();

			}

		}

		document.push(buffer.clone());
		buffer.clear();

	}

	return (message, document);

}

// pub fn scrambleDocument(document: Vec<Vec<Vec<String>>>, key: Vec<Vec<String>>) -> Vec<Vec<Vec<String>>> {
pub fn scrambleDocument(mut document: Vec<Vec<Vec<String>>>, key: Vec<Vec<String>>, rounds: i8) {

	let mut lock = key.clone();

	for block in document.iter_mut() {

		*block = XOR(block.to_vec(), key.clone());

		for round in 1..=rounds {

			// let mut lock = shuffleVector(key[0][0].clone());
			lock = scheduleKey(lock, round);

		}

	}

}

fn shuffleBits(bits: String) -> String {

	let mut rng = rand::thread_rng();
	let mut word = String::from(&bits);
	let mut address_a;
	let mut address_b;
	let mut bit_a;
	let mut bit_b;

	for _ in 0..bits.len() {

		address_a = rng.gen_range(0..bits.len());
		bit_a = word.chars().nth(address_a).unwrap();
		address_b = rng.gen_range(0..bits.len());
		bit_b = word.chars().nth(address_b).unwrap();

		while bit_b == bit_a || address_b == address_a {

			address_b = rng.gen_range(0..bits.len());
			bit_b = word.chars().nth(address_b).unwrap();

		}

		word.replace_range(address_a..address_a + 1, &bit_b.to_string());
		word.replace_range(address_b..address_b + 1, &bit_a.to_string());

	}

	return word;

}

fn partitionBits(bits: String) -> Vec<String> {

	let mut sections = vec![];

	for byte in (0..bits.len()).step_by(8) {

		sections.push(format!("{:0width$x}",
							  u32::from_str_radix(&bits[byte..byte + 8], 2).unwrap(),
							  width = 2));

	}

	return sections;

}

fn stackBytes(bits: String) -> Vec<Vec<String>> {

	let blocks = partitionBits(bits);
	let mut matrix = vec![];

	for block in blocks.chunks(4) {

		matrix.push(block.to_vec());

	}

	return matrix;

}

fn encodeDocument(message: String) -> String {

	let mut hex = String::new();

	for character in message.chars() {

		hex.push_str(&format!("{:02x}", character as u32));

	}

	return hex;

}

fn shuffleVector(mut word: Vec<String>, round: i8) -> Vec<String> {

	let constant = constants::roundConstants.get(&round).unwrap();
	word = leftShift(word);
	word = forwardSubstitution(word);
	word = xor(word, constant.clone());
	return word;

}

pub fn leftShift(mut word: Vec<String>) -> Vec<String> {

	let buffer = word.remove(0);
	word.push(buffer);
	return word;

}

pub fn formatIndex(character: String) -> (String, String) {

	let mut row = character.chars().nth(0).unwrap().to_string();
	let mut column = character.chars().nth(1).unwrap().to_string();
	row.push_str("0");
	column = "0".to_owned() + &column;
	return (row, column);

}

pub fn forwardSubstitution(mut word: Vec<String>) -> Vec<String> {

	for character in word.iter_mut() {

		let (row, column) = formatIndex(character.clone());
		*character = constants::sBox.get(&(&row, &column)).unwrap().to_string();

	}

	return word;

}

fn xor(mut word: Vec<String>, constant: Vec<&str>) -> Vec<String> {

	let binary = u8::from_str_radix(&word[0], 16).unwrap();
	let vector = u8::from_str_radix(&constant[0], 16).unwrap();
	let sum = binary ^ vector;
	word[0] = format!("{:02x}", sum);
	return word;

}

fn XOR(mut data: Vec<Vec<String>>, lock: Vec<Vec<String>>) -> Vec<Vec<String>> {

	for (row, array) in data.iter_mut().enumerate() {

		for (column, character) in array.iter_mut().enumerate() {

			let binary = u8::from_str_radix(&character.to_string(), 16).unwrap();
			let vector = u8::from_str_radix(&lock[row][column].to_owned(), 16).unwrap();
			let sum = binary ^ vector;
			*character = format!("{:02x}", sum).to_string();

		}

	}

	return data;

}

fn scheduleKey(mut key: Vec<Vec<String>>, round: i8) -> Vec<Vec<String>> {

	*key.last_mut().unwrap() = shuffleVector(key.last().unwrap().clone(), round);
	return key;

}
