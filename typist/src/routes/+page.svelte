<script lang="ts">
const keys = $state({ value: [] });
const keyCode = $state({ value: "" });

const websocket = new WebSocket("ws://192.168.31.2:1968");
websocket.onopen = () => {
	websocket.send("typist");
};
websocket.onmessage = ({ data }) => {
	if (data.startsWith("assigned")) {
		const args = data.split(" ");
		keys.value = args.slice(1);
	}
};

function pressKey(key: string) {
	websocket.send(`press ${key}`);
}

document.onkeydown = (e) => {
	keyCode.value = e.key;
};
</script>

{#each keys.value as key}
	<button onclick={() => pressKey(key)} class="bg-neutral-300 p-3 m-1">{key}</button>
{/each}
<p>{keyCode.value}</p>
