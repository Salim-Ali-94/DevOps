import styles from "./styles.module.css";


export default function ItemModal({ setVisible }) {

    return (

        <div className={styles.overlay}>

            {/* <div className={styles.modal}> */}

                <form className={styles.modal}>

                    <label className={styles.headingText}>Add a new item to your checklist</label>

                    <input className={styles.inputField}
                           placeholder="New item"
                           type="text"/>

                    <button className={styles.submitButton}
                            onClick={() => setVisible(false)}>Submit</button>

                </form>


            {/* </div> */}

        </div>

    );

}
