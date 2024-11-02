<template>
    <div>
        <Head>
            <Title>{{ props.title }} | Theft Prediction</Title>
            <Meta name="description" :content="props.description" />
        </Head>
    </div>
</template>

<script setup>
const props = defineProps({
    title: '',
    description: ''
})

</script>