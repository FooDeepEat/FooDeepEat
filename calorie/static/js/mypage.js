
const energy = document.getElementById("total_energy").innerHTML;
const carbohydrate = document.getElementById('total_carbohydrate').innerHTML;
const protein = document.getElementById('total_protein').innerHTML;
const fat = document.getElementById('total_fat').innerHTML;


const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

var width = canvas.clientWidth;
var height = canvas.clientHeight;

var value = [
    {number : parseInt(carbohydrate), text : '탄수화물'},
    {number : parseInt(protein), text : '단백질'},
    {number : parseInt(fat), text : '지방'},
];

console.log(value);

var degree = 360;
var radius = width * 0.7 / 2;

if(radius > height * 0.7 / 2){
    radius = height * 0.7 / 2;
}

const colorArray = ['#F38181', '#FCE38A', '#95E1D3'];

var sum = 0;
value.forEach( arg=> sum+= arg.number);

var conv_array = value.slice().map((data)=>{
    var rate = data.number / sum;
    var myDegree = degree * rate;
    return myDegree;
});

degree = 0;
var event_array = value.slice().map( arg=> []);


var current = -1;
var zero = 0;

var clr = setInterval(() => {
    for(var i=0;i < conv_array.length;i++){
        var item = conv_array[i];
        if(current == -1|| current == i){
            current = i;
            if(zero < item){
                if(i == 0){
                    arcMaker(radius, 0, zero, colorArray[i]);
                } else {
                    arcMaker(radius, degree, degree+zero, colorArray[i]);
                }
                zero+=3;             
            } else {
                current = i+1;
                zero = 0;
                if(i != 0){
                    arcMaker(radius, degree, degree + item, colorArray[i]);
                    event_array[i] = [degree, degree+item];
                    degree =  degree + item;     
                } else {
                    arcMaker(radius, 0, item, colorArray[i]);
                    degree = item;
                    event_array[i] = [0, degree];
                }
            }                               
        } else if (current == conv_array.length){
            clearInterval(clr);
            makeText(-1);
        } 
    }
}, 1);


function arcMaker(radius, begin, end, color){
    ctx.save();
    ctx.lineJoin = 'round';
    ctx.lineWidth = 4; 
    ctx.beginPath();
    ctx.moveTo(width/2, height/2);                           
    ctx.arc(width/2, height/2, radius, (Math.PI/180)*begin, (Math.PI/180)* end , false);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.strokeStyle = 'white';
    ctx.fill();
    ctx.stroke();
    ctx.restore();        
    middelMaker();
}


var drawed = false;
// canvas.addEventListener('mousemove', function (event) {
//     var x1 = event.clientX - canvas.offsetLeft;
//     var y1 = event.clientY - canvas.offsetTop;
//     var inn = isInsideArc(x1, y1);
//     if(inn.index > -1){
//         drawed = true;
//         hoverCanvas(inn.index);
//         makeText(inn.index);
//     } else {
//         if(drawed){
//             hoverCanvas(-1);
//             makeText(-1);
//         }
//         drawed = false;
//     }
// }); 

function isInsideArc(x1, y1){
    var result1 = false;
    var result2 = false;
    var index = -1;
    var circle_len = radius;
    var x = width/2 - x1;
    var y = height/2 - y1;
    var my_len = Math.sqrt(Math.abs(x * x) + Math.abs(y * y));
    if(circle_len >= my_len){
        result1 = true;
    }            
    var rad = Math.atan2(y, x);
    rad = (rad*180)/Math.PI;
    rad += 180;
    if(result1){
        event_array.forEach( (arr,idx) => {
            if( rad >= arr[0] && rad <= arr[1]){
                result2 = true;
                index = idx;
            }
        });
    }
    return {result1:result1, result2:result2 ,index:index, degree : rad};
}


// function hoverCanvas(index){
//     ctx.clearRect(0,0,width, height);
//     for (var i = 0; i < conv_array.length; i++) {
//         var item = conv_array[i];
//         var innRadius = radius;
//         if(index == i){  
//             innRadius = radius * 1.1;
//         }
//         if (i == 0) {
//             arcMaker(innRadius, 0, item, colorArray[i])
//             degree = item;
//         } else {
//             arcMaker(innRadius, degree, degree + item, colorArray[i])
//             degree = degree + item;
//         }
//     }
// }

function degreesToRadians(degrees) {
    const pi = Math.PI;
    return degrees * (pi / 180);
}


function makeText(index){
    event_array.forEach((itm, idx) => {
        var half = (itm[1] - itm[0]) / 2;
        var degg = itm[0] + half;
        var xx = Math.cos(degreesToRadians(degg)) * radius * 0.7 + width / 2;
        var yy = Math.sin(degreesToRadians(degg)) * radius * 0.7 + height / 2;

        var txt = value[idx].text + '';
        var minus = ctx.measureText(txt).width / 2;
        ctx.save();
        if(index == idx){
            ctx.font = "100 14px Roboto";
            ctx.fillStyle = '#1a1a1a';
        } else {
            ctx.font = "100 14px Roboto";
            ctx.fillStyle = '#1a1a1a';
        }
        ctx.fillText(txt, xx - minus, yy);
        var txt2 = value[idx].number;
        ctx.fillText(txt2, xx - ctx.measureText(txt2).width / 3, yy + 16);
        ctx.restore();
    });
}


function middelMaker(){
    ctx.save();
    ctx.fillStyle='white';
    ctx.strokeStyle='white';
    ctx.lineJoin = 'round';
    ctx.lineWidth = 1; 
    ctx.beginPath();
    ctx.moveTo(width/2, height/2);
    ctx.arc(width/2, height/2, radius/3, (Math.PI/180)*0, (Math.PI/180)* 360 , false);
    ctx.fill();
    ctx.stroke();
    ctx.closePath();
    ctx.restore();

    var total = 0;
    value.forEach( (arg)=> total+=arg.number);
    var minus = ctx.measureText(total).width; 
    ctx.save();
    ctx.font = "400 16px Roboto";
    ctx.fillStyle = '#1a1a1a';
    ctx.fillText("열량", width/2 - ctx.measureText("열량").width/2, height/2);
    ctx.fillText(total, width/2 - 0.8*minus, height/2 * 1.1);
    ctx.restore();
}




