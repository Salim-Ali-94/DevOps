import styles from "./styles.module.css"


export default function AddButton({addHandler}) {

    return (

        <button className={styles.container}
                onClick={addHandler}>+ New task</button>

    );

}