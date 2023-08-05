import styles from "./styles.module.css";


export default function ItemModal({ setVisible }) {

    return (

        <div className={styles.overlay}>

            <div className={styles.modal}>

                <h1>INPUT TEXT</h1>
                <button onClick={() => setVisible(false)}>Close</button>

            </div>

        </div>

    );

}
